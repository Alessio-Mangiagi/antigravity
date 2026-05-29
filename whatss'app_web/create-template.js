const ExcelJS = require('exceljs');
const path = require('path');

async function createTemplate() {
    const workbook = new ExcelJS.Workbook();
    const sheet = workbook.addWorksheet('Contatti');

    // Intestazioni
    sheet.columns = [
        { header: 'Nome', key: 'nome', width: 25 },
        { header: 'Gruppo WhatsApp', key: 'gruppo', width: 30 },
        { header: 'Compleanno', key: 'compleanno', width: 18 },
        { header: 'Messaggio', key: 'messaggio', width: 60 }
    ];

    // Stile intestazione
    sheet.getRow(1).font = { bold: true };
    sheet.getRow(1).fill = {
        type: 'pattern',
        pattern: 'solid',
        fgColor: { argb: 'FF25D366' }
    };
    sheet.getRow(1).font = { bold: true, color: { argb: 'FFFFFFFF' } };

    // Dati di esempio
    const esempi = [
        {
            nome: 'Mario Rossi',
            gruppo: 'Famiglia',
            compleanno: new Date(1990, 2, 15), // 15 marzo 1990
            messaggio: 'Tanti auguri Mario! 🎉 Che tu possa avere una giornata fantastica!'
        },
        {
            nome: 'Luca Bianchi',
            gruppo: 'Amici calcetto',
            compleanno: new Date(1988, 5, 22),
            messaggio: 'Auguri Luca! 🎂🎊'
        },
        {
            nome: 'Anna Verdi',
            gruppo: 'Lavoro',
            compleanno: new Date(1995, 10, 8),
            messaggio: 'Buon compleanno Anna! 🥳'
        }
    ];

    esempi.forEach(row => {
        const addedRow = sheet.addRow(row);
        addedRow.getCell('compleanno').numFmt = 'DD/MM/YYYY';
    });

    // Nota istruzione
    sheet.getRow(sheet.lastRow.number + 2).getCell(1).value =
        '⚠ NOTA: Il campo "Gruppo WhatsApp" deve corrispondere ESATTAMENTE al nome del gruppo (maiuscole/minuscole incluse)';

    const outputPath = path.join(__dirname, 'contacts.xlsx');
    await workbook.xlsx.writeFile(outputPath);
    console.log(`Template creato: ${outputPath}`);
    console.log('Modifica il file con i tuoi contatti, poi esegui: npm start');
}

createTemplate().catch(console.error);
