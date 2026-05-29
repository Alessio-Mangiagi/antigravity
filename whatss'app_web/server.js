const express = require('express');
const http = require('http');
const { Server } = require('socket.io');
const QRCode = require('qrcode');
const path = require('path');
const { Client, LocalAuth } = require('whatsapp-web.js');
const L = require('./logica');

const PORT = 3000;

const app = express();
const server = http.createServer(app);
const io = new Server(server);

app.use(express.static(path.join(__dirname, 'public')));

// ---------- Stato globale ----------
let stato = {
    connessione: 'avvio',      // avvio | qr | caricamento | connesso | errore | disconnesso
    qrDataUrl: null,
    caricamento: 0,
    dati: null,                // { persone, frasiSingole, frasiGruppo }
    festeggiati: [],
    anteprima: null,
    gruppoTrovato: null,
    gruppiDisponibili: []
};

const logBuffer = [];
function log(msg, tipo = 'info') {
    const riga = { ts: new Date().toLocaleTimeString('it-IT'), msg, tipo };
    logBuffer.push(riga);
    if (logBuffer.length > 200) logBuffer.shift();
    io.emit('log', riga);
    console.log(`[${riga.ts}] ${msg}`);
}

function pushStato() {
    io.emit('stato', stato);
}

// ---------- Caricamento dati Excel + calcolo compleanni ----------
async function ricaricaDati() {
    try {
        stato.dati = await L.leggiDati();
        stato.festeggiati = stato.dati.persone
            .filter(p => L.eCompleannoOggi(p.dataNascita))
            .map(p => ({ nome: L.nomeCompleto(p), data: L.formattaData(p.dataNascita) }));

        // costruisci anteprima messaggio
        const festObj = stato.dati.persone.filter(p => L.eCompleannoOggi(p.dataNascita));
        if (festObj.length > 0) {
            const usaGruppo = festObj.length > 1;
            const frase = L.fraseCasuale(usaGruppo ? stato.dati.frasiGruppo : stato.dati.frasiSingole);
            stato.anteprima = L.costruisciMessaggio(festObj, frase);
        } else {
            stato.anteprima = null;
        }

        log(`Dati caricati: ${stato.dati.persone.length} persone, ${stato.dati.frasiSingole.length} frasi singole, ${stato.dati.frasiGruppo.length} frasi gruppo`, 'ok');
        log(`Compleanni oggi: ${stato.festeggiati.length}`, stato.festeggiati.length ? 'ok' : 'info');
        pushStato();
    } catch (err) {
        log(`Errore lettura Excel: ${err.message}`, 'errore');
        pushStato();
    }
}

// ---------- WhatsApp client ----------
const client = new Client({
    authStrategy: new LocalAuth({ dataPath: '.wwebjs_auth' }),
    puppeteer: { headless: true, args: ['--no-sandbox', '--disable-setuid-sandbox'] }
});

client.on('qr', async (qr) => {
    stato.connessione = 'qr';
    try {
        stato.qrDataUrl = await QRCode.toDataURL(qr, { width: 300, margin: 2 });
    } catch (e) {
        stato.qrDataUrl = null;
    }
    log('QR generato. Scansiona con WhatsApp (Impostazioni → Dispositivi collegati).', 'info');
    pushStato();
});

client.on('loading_screen', (percent) => {
    stato.connessione = 'caricamento';
    stato.caricamento = parseInt(percent) || 0;
    pushStato();
});

client.on('authenticated', () => {
    stato.qrDataUrl = null;
    log('Autenticato! Sessione salvata.', 'ok');
    pushStato();
});

client.on('ready', async () => {
    stato.connessione = 'connesso';
    stato.qrDataUrl = null;
    log('WhatsApp connesso!', 'ok');

    try {
        const chats = await client.getChats();
        const gruppi = chats.filter(c => c.isGroup);
        stato.gruppiDisponibili = gruppi.map(g => g.name);
        const target = gruppi.find(g =>
            g.name.toLowerCase().trim() === L.CONFIG.GRUPPO_DESTINAZIONE.toLowerCase().trim()
        );
        stato.gruppoTrovato = target ? target.name : null;
        if (target) {
            log(`Gruppo destinazione trovato: "${target.name}"`, 'ok');
        } else {
            log(`Gruppo "${L.CONFIG.GRUPPO_DESTINAZIONE}" NON trovato tra i ${gruppi.length} gruppi.`, 'errore');
        }
    } catch (e) {
        log(`Errore lettura gruppi: ${e.message}`, 'errore');
    }
    pushStato();
});

client.on('auth_failure', () => {
    stato.connessione = 'errore';
    log('Autenticazione fallita. Elimina cartella .wwebjs_auth e riavvia.', 'errore');
    pushStato();
});

client.on('disconnected', (reason) => {
    stato.connessione = 'disconnesso';
    log(`Disconnesso: ${reason}`, 'errore');
    pushStato();
});

// ---------- Invio auguri ----------
async function inviaAuguri() {
    if (stato.connessione !== 'connesso') {
        log('Impossibile inviare: WhatsApp non connesso.', 'errore');
        return { ok: false, msg: 'WhatsApp non connesso' };
    }
    const festObj = stato.dati ? stato.dati.persone.filter(p => L.eCompleannoOggi(p.dataNascita)) : [];
    if (festObj.length === 0) {
        log('Nessun compleanno oggi, niente da inviare.', 'info');
        return { ok: false, msg: 'Nessun compleanno oggi' };
    }

    try {
        const chats = await client.getChats();
        const gruppi = chats.filter(c => c.isGroup);
        const target = gruppi.find(g =>
            g.name.toLowerCase().trim() === L.CONFIG.GRUPPO_DESTINAZIONE.toLowerCase().trim()
        );
        if (!target) {
            log(`Gruppo "${L.CONFIG.GRUPPO_DESTINAZIONE}" non trovato.`, 'errore');
            return { ok: false, msg: 'Gruppo non trovato' };
        }
        const messaggio = stato.anteprima || L.costruisciMessaggio(
            festObj, L.fraseCasuale(festObj.length > 1 ? stato.dati.frasiGruppo : stato.dati.frasiSingole)
        );
        await target.sendMessage(messaggio);
        log(`[OK] Auguri inviati a "${target.name}" per: ${L.unisciNomi(festObj)}`, 'ok');
        return { ok: true, msg: 'Inviato!' };
    } catch (err) {
        log(`Invio fallito: ${err.message}`, 'errore');
        return { ok: false, msg: err.message };
    }
}

// ---------- Socket.io ----------
io.on('connection', (socket) => {
    socket.emit('stato', stato);
    socket.emit('config', { gruppo: L.CONFIG.GRUPPO_DESTINAZIONE, excel: L.CONFIG.EXCEL_FILE });
    logBuffer.forEach(r => socket.emit('log', r));

    socket.on('invia', async () => {
        const res = await inviaAuguri();
        socket.emit('risultatoInvio', res);
    });

    socket.on('ricarica', async () => {
        await ricaricaDati();
    });
});

// ---------- Avvio ----------
server.listen(PORT, async () => {
    log(`Interfaccia web attiva su http://localhost:${PORT}`, 'ok');
    await ricaricaDati();
    log('Avvio motore WhatsApp...', 'info');
    client.initialize().catch(e => {
        stato.connessione = 'errore';
        log(`Errore avvio Chromium: ${e.message}`, 'errore');
        pushStato();
    });
});
