@echo off
cd /d "%~dp0"
echo Avvio WhatsApp Auguri...
echo Interfaccia web: http://localhost:3000
echo.
start "" http://localhost:3000
node server.js
echo.
echo === Server terminato ===
pause
