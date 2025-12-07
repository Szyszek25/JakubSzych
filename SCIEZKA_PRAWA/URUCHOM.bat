@echo off
echo ========================================
echo   SCIEZKA PRAWA - Uruchomienie API
echo ========================================
echo.

cd /d "%~dp0"

REM Sprawdź czy Python jest zainstalowany
python --version >nul 2>&1
if errorlevel 1 (
    echo [BLAD] Python nie jest zainstalowany!
    echo Zainstaluj Python 3.9+ z https://www.python.org/
    pause
    exit /b 1
)

REM Sprawdź czy venv istnieje
if not exist "venv\" (
    echo [INFO] Tworzenie wirtualnego środowiska...
    python -m venv venv
    if errorlevel 1 (
        echo [BLAD] Nie mozna utworzyc venv!
        pause
        exit /b 1
    )
)

REM Aktywuj venv
echo [INFO] Aktywacja wirtualnego środowiska...
call venv\Scripts\activate.bat

REM Zainstaluj zależności
if not exist "venv\Lib\site-packages\fastapi" (
    echo [INFO] Aktualizacja pip...
    python -m pip install --upgrade pip setuptools wheel
    
    echo [INFO] Instalacja zależności...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [BLAD] Nie mozna zainstalowac zaleznosci!
        echo [INFO] Probuje zainstalowac podstawowe pakiety...
        pip install fastapi uvicorn[standard] pydantic python-multipart
        if errorlevel 1 (
            pause
            exit /b 1
        )
    )
)

REM Uruchom API
echo.
echo [INFO] Uruchamianie API...
echo [INFO] API będzie dostępne pod: http://localhost:8003
echo [INFO] Dokumentacja: http://localhost:8003/docs
echo.
echo Naciśnij Ctrl+C aby zatrzymać serwer
echo.

python api.py

pause

