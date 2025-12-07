@echo off
REM 📦 ZANT - Instalacja środowiska
echo.
echo ============================================================
echo 📦 ZANT - INSTALACJA ŚRODOWISKA
echo ============================================================
echo.

REM Sprawdź Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python nie jest zainstalowany!
    echo Zainstaluj Python 3.10+ z https://www.python.org/
    pause
    exit /b 1
)

echo ✅ Python wykryty
python --version
echo.

REM Sprawdź Google API Key
if "%GOOGLE_API_KEY%"=="" (
    echo ⚠️  UWAGA: GOOGLE_API_KEY nie jest ustawione
    echo.
    echo Ustaw zmienną środowiskową przed uruchomieniem:
    echo   set GOOGLE_API_KEY=twój_klucz
    echo.
    echo LUB utwórz plik .env z:
    echo   GOOGLE_API_KEY=twój_klucz
    echo.
    echo Uzyskaj klucz na: https://aistudio.google.com/
    echo.
)
echo.

REM Utwórz venv jeśli nie istnieje
if not exist "venv\Scripts\python.exe" (
    echo [1/3] Tworzenie środowiska wirtualnego...
    python -m venv venv
    if errorlevel 1 (
        echo ❌ Nie udało się utworzyć venv
        pause
        exit /b 1
    )
    echo ✅ Venv utworzone
) else (
    echo ✅ Venv już istnieje
)
echo.

REM Aktywuj venv
echo [2/3] Aktywacja środowiska...
call venv\Scripts\activate.bat
echo ✅ Środowisko aktywowane
echo.

REM Zainstaluj wymagania
echo [3/3] Instalowanie zależności...
pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Nie udało się zainstalować zależności
    pause
    exit /b 1
)
echo.

echo ============================================================
echo ✅ INSTALACJA ZAKOŃCZONA POMYŚLNIE!
echo ============================================================
echo.
echo Aby uruchomić projekt:
echo   URUCHOM.bat
echo   LUB
echo   cd backend
echo   python -m api.main
echo.
pause

