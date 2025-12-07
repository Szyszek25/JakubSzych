@echo off
REM Skrypt do aktywacji wirtualnego srodowiska

cd /d "%~dp0"

if not exist "venv\Scripts\activate.bat" (
    echo Wirtualne srodowisko nie istnieje!
    echo Uruchom najpierw: setup_venv.bat
    pause
    exit /b 1
)

echo Aktywowanie wirtualnego srodowiska...
call venv\Scripts\activate.bat

echo.
echo Wirtualne srodowisko aktywowane!
echo Aby dezaktywowac wpisz: deactivate
echo.

REM Uruchomienie PowerShell z aktywnym venv
powershell -NoExit -Command "cd '$PWD'; Write-Host 'Wirtualne srodowisko aktywowane!' -ForegroundColor Green"

