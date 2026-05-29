const { Client, LocalAuth } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');

console.log('Test avvio motore WhatsApp (Chromium)...');

const client = new Client({
    authStrategy: new LocalAuth({ dataPath: '.wwebjs_auth' }),
    puppeteer: { headless: true, args: ['--no-sandbox', '--disable-setuid-sandbox'] }
});

client.on('qr', () => {
    console.log('[OK] Motore funziona! QR generato (sessione non ancora collegata).');
    client.destroy().then(() => process.exit(0));
});

client.on('authenticated', () => {
    console.log('[OK] Motore funziona + sessione gia collegata!');
    client.destroy().then(() => process.exit(0));
});

client.on('ready', () => {
    console.log('[OK] WhatsApp pronto e connesso!');
    client.destroy().then(() => process.exit(0));
});

client.initialize().catch(e => {
    console.error('[ERRORE] Chromium/puppeteer fallito:', e.message);
    process.exit(1);
});

setTimeout(() => {
    console.error('[TIMEOUT] Nessun evento dopo 90s. Possibile problema Chromium.');
    process.exit(1);
}, 90000);
