@echo off
NET SESSION >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

set TASK_NAME=WhatsAppWeb_Avvio

schtasks /delete /tn "%TASK_NAME%" /f
del /f "%~dp0avvia_nascosto.vbs" 2>nul

echo [OK] Avvio automatico rimosso.
pause
