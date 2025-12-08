@echo off
REM 🚀 GQPA-Indeks Branż - Szybkie uruchomienie (Windows)

echo.
echo ============================================================
echo 🏦 GQPA-INDEKS BRANŻ - SYSTEM ANALIZY KONDYCJI BRANŻ
echo ============================================================
echo.

REM Sprawdź czy Python jest dostępny
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python nie jest zainstalowany lub nie jest w PATH
    pause
    exit /b 1
)

REM Sprawdź czy venv istnieje
if not exist "venv\Scripts\python.exe" (
    echo 📦 Tworzenie środowiska wirtualnego...
    python -m venv venv
    if errorlevel 1 (
        echo ❌ Nie udało się utworzyć venv
        pause
        exit /b 1
    )
)

REM Aktywuj venv
call venv\Scripts\activate.bat

REM Sprawdź czy wymagania są zainstalowane
python -c "import pandas" >nul 2>&1
if errorlevel 1 (
    echo 📥 Instalowanie wymagań...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ Nie udało się zainstalować wymagań
        pause
        exit /b 1
    )
)

REM Uruchom główny skrypt
echo.
echo 🚀 Uruchamianie analizy...
echo.
python main.py --full

echo.
echo ✅ Zakończono!
echo.
pause


