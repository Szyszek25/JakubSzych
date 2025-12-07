@echo off
echo ========================================
echo Tworzenie wirtualnego srodowiska Python
echo ========================================
echo.

cd /d "%~dp0"

REM Sprawdzenie czy venv juz istnieje
if exist "venv" (
    echo Wirtualne srodowisko juz istnieje!
    echo.
    echo Aby aktywowac: venv\Scripts\activate.bat
    echo Aby dezaktywowac: deactivate
    pause
    exit /b
)

echo Tworzenie wirtualnego srodowiska...
python -m venv venv

if errorlevel 1 (
    echo BLAD: Nie udalo sie utworzyc wirtualnego srodowiska!
    echo Sprawdz czy Python jest zainstalowany.
    pause
    exit /b 1
)

echo.
echo Aktywowanie wirtualnego srodowiska...
call venv\Scripts\activate.bat

echo.
echo Aktualizacja pip...
python -m pip install --upgrade pip

echo.
echo Instalowanie zaleznosci z requirements.txt...
python -m pip install -r requirements.txt

echo.
echo ========================================
echo Wirtualne srodowisko utworzone!
echo ========================================
echo.
echo Aby aktywowac w przyszlosci:
echo   venv\Scripts\activate.bat
echo.
echo Aby dezaktywowac:
echo   deactivate
echo.
pause

