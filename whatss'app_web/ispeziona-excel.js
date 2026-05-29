const ExcelJS = require('exceljs');

async function ispeziona() {
    const wb = new ExcelJS.Workbook();
    await wb.xlsx.readFile('C:\\Users\\aless\\Documents\\Compleanni_e_Auguri.xlsx');

    wb.eachSheet((sheet, id) => {
        console.log(`\n=== Foglio ${id}: "${sheet.name}" ===`);
        const header = sheet.getRow(1);
        console.log('Colonne:');
        header.eachCell((cell, col) => {
            console.log(`  [${col}] ${cell.value}`);
        });
        console.log('\nPrime 3 righe dati:');
        for (let r = 2; r <= 4; r++) {
            const row = sheet.getRow(r);
            const vals = [];
            row.eachCell((cell, col) => vals.push(`[${col}]=${JSON.stringify(cell.value)}`));
            if (vals.length) console.log(`  Riga ${r}: ${vals.join('  ')}`);
        }
    });
}

ispeziona().catch(console.error);
