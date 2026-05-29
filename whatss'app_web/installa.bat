@echo off
:: Richiede privilegi admin
NET SESSION >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Richiesta elevazione privilegi...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

set TASK_NAME=WhatsAppWeb_Avvio
set SCRIPT_PATH=%~dp0avvia_nascosto.vbs

:: Crea VBScript per avvio silenzioso (nessuna finestra cmd)
echo Set oShell = CreateObject("WScript.Shell") > "%SCRIPT_PATH%"
echo oShell.Run "cmd /c cd /d ""%~dp0"" && node server.js", 0, False >> "%SCRIPT_PATH%"

:: Registra task scheduler al login utente
schtasks /create /tn "%TASK_NAME%" /tr "wscript.exe \"%SCRIPT_PATH%\"" /sc onlogon /ru "%USERNAME%" /f

if %ERRORLEVEL% EQU 0 (
    echo.
    echo [OK] Task registrato: %TASK_NAME%
    echo [OK] Si avviera automaticamente al prossimo login.
) else (
    echo [ERRORE] Registrazione fallita.
)
pause
