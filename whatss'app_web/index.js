const { Client, LocalAuth } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');
const ExcelJS = require('exceljs');

// ======================= CONFIG =======================
const CONFIG = {
    // Percorso del file Excel con i dati
    EXCEL_FILE: 'C:\\Users\\aless\\Documents\\Compleanni_e_Auguri.xlsx',

    // ⚠ IMPOSTA QUI: nome ESATTO del gruppo WhatsApp dove inviare gli auguri
    // (maiuscole/minuscole non contano, ma il nome deve corrispondere)
    GRUPPO_DESTINAZIONE: 'NOME_DEL_TUO_GRUPPO',

    // Nomi dei fogli nel file Excel
    FOGLIO_COMPLEANNI: 'Compleanni',
    FOGLIO_FRASI_SINGOLE: 'Frasi di auguri',
    FOGLIO_FRASI_GRUPPO: 'Auguri di gruppo'
};
// ======================================================

// ---------- Lettura dati Excel ----------
async function leggiDati() {
    const wb = new ExcelJS.Workbook();
    await wb.xlsx.readFile(CONFIG.EXCEL_FILE);

    // Foglio 1: persone (Nome, Cognome, Data di nascita)
    const fComp = wb.getWorksheet(CONFIG.FOGLIO_COMPLEANNI);
    if (!fComp) throw new Error(`Foglio "${CONFIG.FOGLIO_COMPLEANNI}" non trovato`);

    const persone = [];
    fComp.eachRow((row, n) => {
        if (n === 1) return; // intestazione
        const nome = row.getCell(1).value;
        const cognome = row.getCell(2).value;
        const dataNascita = row.getCell(3).value;
        if (nome && dataNascita) {
            persone.push({
                nome: String(nome).trim(),
                cognome: cognome ? String(cognome).trim() : '',
                dataNascita
            });
        }
    });

    // Foglio 2: frasi singole
    const frasiSingole = leggiPoolFrasi(wb, CONFIG.FOGLIO_FRASI_SINGOLE);
    // Foglio 3: frasi gruppo
    const frasiGruppo = leggiPoolFrasi(wb, CONFIG.FOGLIO_FRASI_GRUPPO);

    return { persone, frasiSingole, frasiGruppo };
}

function leggiPoolFrasi(wb, nomeFoglio) {
    const foglio = wb.getWorksheet(nomeFoglio);
    if (!foglio) throw new Error(`Foglio "${nomeFoglio}" non trovato`);
    const frasi = [];
    foglio.eachRow((row, n) => {
        if (n === 1) return; // intestazione
        const frase = row.getCell(2).value; // colonna B = frase
        if (frase) frasi.push(String(frase).trim());
    });
    return frasi;
}

// ---------- Logica compleanno (UTC per evitare slittamento fuso orario) ----------
function eCompleannoOggi(dataValue) {
    const oggi = new Date();
    let bday;

    if (dataValue instanceof Date) {
        // Excel salva date a mezzanotte UTC → uso giorno/mese UTC
        return dataValue.getUTCDate() === oggi.getDate() &&
               dataValue.getUTCMonth() === oggi.getMonth();
    } else if (typeof dataValue === 'string') {
        const slash = dataValue.split('/');
        const dash = dataValue.split('-');
        if (slash.length === 3) {
            bday = new Date(slash[2], slash[1] - 1, slash[0]);
        } else if (dash.length === 3) {
            bday = new Date(dash[0], dash[1] - 1, dash[2].slice(0, 2));
        } else {
            return false;
        }
    } else if (typeof dataValue === 'number') {
        bday = new Date((dataValue - 25569) * 86400 * 1000);
        return bday.getUTCDate() === oggi.getDate() &&
               bday.getUTCMonth() === oggi.getMonth();
    } else {
        return false;
    }

    if (isNaN(bday.getTime())) return false;
    return bday.getDate() === oggi.getDate() && bday.getMonth() === oggi.getMonth();
}

// ---------- Costruzione messaggio ----------
function fraseCasuale(pool) {
    if (!pool || pool.length === 0) return 'Tanti auguri di buon compleanno! 🎉🎂';
    return pool[Math.floor(Math.random() * pool.length)];
}

function nomeCompleto(p) {
    return p.cognome ? `${p.nome} ${p.cognome}` : p.nome;
}

// Unisce nomi in italiano: "A, B e C"
function unisciNomi(persone) {
    const nomi = persone.map(nomeCompleto);
    if (nomi.length === 1) return nomi[0];
    return nomi.slice(0, -1).join(', ') + ' e ' + nomi[nomi.length - 1];
}

// Inserisce i nomi nella frase: usa segnaposto {nome} se presente, altrimenti prepende intestazione
function costruisciMessaggio(persone, frase) {
    if (frase.includes('{nome}')) {
        return frase.replace(/\{nome\}/g, unisciNomi(persone));
    }
    return `🎉 ${unisciNomi(persone)}!\n\n${frase}`;
}

// ---------- Main ----------
async function main() {
    console.log('=== WhatsApp Auguri ===');
    console.log(`Data: ${new Date().toLocaleDateString('it-IT')}\n`);

    if (CONFIG.GRUPPO_DESTINAZIONE === 'NOME_DEL_TUO_GRUPPO') {
        console.error('⚠ Devi impostare GRUPPO_DESTINAZIONE in cima a index.js!');
        process.exit(1);
    }

    let dati;
    try {
        dati = await leggiDati();
        console.log(`Persone caricate: ${dati.persone.length}`);
        console.log(`Frasi singole: ${dati.frasiSingole.length} | Frasi gruppo: ${dati.frasiGruppo.length}`);
    } catch (err) {
        console.error(`Errore lettura Excel: ${err.message}`);
        process.exit(1);
    }

    const festeggiati = dati.persone.filter(p => eCompleannoOggi(p.dataNascita));

    if (festeggiati.length === 0) {
        console.log('Nessun compleanno oggi. Programma terminato.');
        process.exit(0);
    }

    console.log(`\nCompleanni oggi (${festeggiati.length}):`);
    festeggiati.forEach(p => console.log(`  - ${nomeCompleto(p)}`));

    // Scegli pool: gruppo se >1 festeggiato, singolo altrimenti
    const usaGruppo = festeggiati.length > 1;
    const frase = fraseCasuale(usaGruppo ? dati.frasiGruppo : dati.frasiSingole);
    const messaggio = costruisciMessaggio(festeggiati, frase);

    console.log(`\nMessaggio da inviare al gruppo "${CONFIG.GRUPPO_DESTINAZIONE}":`);
    console.log('-----------------------------------------');
    console.log(messaggio);
    console.log('-----------------------------------------\n');

    const client = new Client({
        authStrategy: new LocalAuth({ dataPath: '.wwebjs_auth' }),
        puppeteer: {
            headless: true,
            args: ['--no-sandbox', '--disable-setuid-sandbox']
        }
    });

    client.on('qr', (qr) => {
        console.log('Prima volta: scansiona QR con WhatsApp (Impostazioni → Dispositivi collegati):\n');
        qrcode.generate(qr, { small: true });
    });

    client.on('loading_screen', (percent) => {
        process.stdout.write(`\rCaricamento WhatsApp: ${percent}%`);
    });

    client.on('authenticated', () => {
        console.log('\nAutenticato! Sessione salvata per le prossime volte.');
    });

    client.on('ready', async () => {
        console.log('WhatsApp connesso!\n');

        const chats = await client.getChats();
        const gruppi = chats.filter(c => c.isGroup);

        const target = gruppi.find(g =>
            g.name.toLowerCase().trim() === CONFIG.GRUPPO_DESTINAZIONE.toLowerCase().trim()
        );

        if (!target) {
            console.log(`[ERRORE] Gruppo "${CONFIG.GRUPPO_DESTINAZIONE}" non trovato.`);
            console.log(`Gruppi disponibili: ${gruppi.map(g => `"${g.name}"`).join(', ')}`);
            await client.destroy();
            process.exit(1);
        }

        try {
            await target.sendMessage(messaggio);
            console.log(`[OK] Auguri inviati al gruppo "${target.name}" per: ${unisciNomi(festeggiati)}`);
        } catch (err) {
            console.log(`[ERRORE] Invio fallito: ${err.message}`);
        }

        await client.destroy();
        process.exit(0);
    });

    client.on('auth_failure', () => {
        console.error('\nAutenticazione fallita. Elimina .wwebjs_auth e riavvia.');
        process.exit(1);
    });

    client.on('disconnected', (reason) => {
        console.log(`Disconnesso: ${reason}`);
    });

    await client.initialize();
}

main().catch(err => {
    console.error('Errore fatale:', err.message);
    process.exit(1);
});
