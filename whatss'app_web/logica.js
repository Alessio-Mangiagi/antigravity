const ExcelJS = require('exceljs');

const CONFIG = {
    EXCEL_FILE: 'C:\\Users\\aless\\Documents\\Compleanni_e_Auguri.xlsx',
    GRUPPO_DESTINAZIONE: 'Prova',
    FOGLIO_COMPLEANNI: 'Compleanni',
    FOGLIO_FRASI_SINGOLE: 'Frasi di auguri',
    FOGLIO_FRASI_GRUPPO: 'Auguri di gruppo'
};

// ---------- Lettura dati Excel ----------
async function leggiDati() {
    const wb = new ExcelJS.Workbook();
    await wb.xlsx.readFile(CONFIG.EXCEL_FILE);

    const fComp = wb.getWorksheet(CONFIG.FOGLIO_COMPLEANNI);
    if (!fComp) throw new Error(`Foglio "${CONFIG.FOGLIO_COMPLEANNI}" non trovato`);

    const persone = [];
    fComp.eachRow((row, n) => {
        if (n === 1) return;
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

    const frasiSingole = leggiPoolFrasi(wb, CONFIG.FOGLIO_FRASI_SINGOLE);
    const frasiGruppo = leggiPoolFrasi(wb, CONFIG.FOGLIO_FRASI_GRUPPO);

    return { persone, frasiSingole, frasiGruppo };
}

function leggiPoolFrasi(wb, nomeFoglio) {
    const foglio = wb.getWorksheet(nomeFoglio);
    if (!foglio) throw new Error(`Foglio "${nomeFoglio}" non trovato`);
    const frasi = [];
    foglio.eachRow((row, n) => {
        if (n === 1) return;
        const frase = row.getCell(2).value;
        if (frase) frasi.push(String(frase).trim());
    });
    return frasi;
}

// ---------- Logica compleanno (UTC per evitare slittamento fuso orario) ----------
function eCompleannoOggi(dataValue) {
    const oggi = new Date();
    let bday;

    if (dataValue instanceof Date) {
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

// ---------- Formattazione data per UI ----------
function formattaData(dataValue) {
    let d;
    if (dataValue instanceof Date) {
        return `${String(dataValue.getUTCDate()).padStart(2, '0')}/${String(dataValue.getUTCMonth() + 1).padStart(2, '0')}/${dataValue.getUTCFullYear()}`;
    } else if (typeof dataValue === 'string') {
        return dataValue.split('T')[0];
    } else if (typeof dataValue === 'number') {
        d = new Date((dataValue - 25569) * 86400 * 1000);
        return `${String(d.getUTCDate()).padStart(2, '0')}/${String(d.getUTCMonth() + 1).padStart(2, '0')}/${d.getUTCFullYear()}`;
    }
    return String(dataValue);
}

// ---------- Costruzione messaggio ----------
function fraseCasuale(pool) {
    if (!pool || pool.length === 0) return 'Tanti auguri di buon compleanno! 🎉🎂';
    return pool[Math.floor(Math.random() * pool.length)];
}

function nomeCompleto(p) {
    return p.cognome ? `${p.nome} ${p.cognome}` : p.nome;
}

function unisciNomi(persone) {
    const nomi = persone.map(nomeCompleto);
    if (nomi.length === 1) return nomi[0];
    return nomi.slice(0, -1).join(', ') + ' e ' + nomi[nomi.length - 1];
}

function costruisciMessaggio(persone, frase) {
    if (frase.includes('{nome}')) {
        return frase.replace(/\{nome\}/g, unisciNomi(persone));
    }
    return `🎉 ${unisciNomi(persone)}!\n\n${frase}`;
}

module.exports = {
    CONFIG,
    leggiDati,
    eCompleannoOggi,
    formattaData,
    fraseCasuale,
    nomeCompleto,
    unisciNomi,
    costruisciMessaggio
};
