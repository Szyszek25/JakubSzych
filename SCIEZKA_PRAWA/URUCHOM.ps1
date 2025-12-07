# Sciezka Prawa - Uruchomienie API (PowerShell)
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  SCIEZKA PRAWA - Uruchomienie API" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Przejdz do katalogu skryptu
Set-Location $PSScriptRoot

# Sprawdz czy Python jest zainstalowany
try {
    $pythonVersion = python --version 2>&1
    Write-Host "[INFO] Znaleziono: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "[BLAD] Python nie jest zainstalowany!" -ForegroundColor Red
    Write-Host "Zainstaluj Python 3.9+ z https://www.python.org/" -ForegroundColor Yellow
    Read-Host "Nacisnij Enter aby zakonczyc"
    exit 1
}

# Sprawdz czy venv istnieje
if (-not (Test-Path "venv")) {
    Write-Host "[INFO] Tworzenie wirtualnego srodowiska..." -ForegroundColor Yellow
    python -m venv venv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[BLAD] Nie mozna utworzyc venv!" -ForegroundColor Red
        Read-Host "Nacisnij Enter aby zakonczyc"
        exit 1
    }
}

# Aktywuj venv
Write-Host "[INFO] Aktywacja wirtualnego srodowiska..." -ForegroundColor Yellow
& "venv\Scripts\Activate.ps1"

# Zainstaluj zaleznosci jesli potrzeba
if (-not (Test-Path "venv\Lib\site-packages\fastapi")) {
    Write-Host "[INFO] Aktualizacja pip..." -ForegroundColor Yellow
    python -m pip install --upgrade pip setuptools wheel
    
    Write-Host "[INFO] Instalacja zaleznosci..." -ForegroundColor Yellow
    pip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[BLAD] Nie mozna zainstalowac zaleznosci!" -ForegroundColor Red
        Write-Host "[INFO] Probuje zainstalowac podstawowe pakiety..." -ForegroundColor Yellow
        pip install fastapi uvicorn[standard] pydantic python-multipart
        if ($LASTEXITCODE -ne 0) {
            Read-Host "Nacisnij Enter aby zakonczyc"
            exit 1
        }
    }
}

# Uruchom API
Write-Host ""
Write-Host "[INFO] Uruchamianie API..." -ForegroundColor Green
Write-Host "[INFO] API bedzie dostepne pod: http://localhost:8003" -ForegroundColor Cyan
Write-Host "[INFO] Dokumentacja: http://localhost:8003/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "Nacisnij Ctrl+C aby zatrzymac serwer" -ForegroundColor Yellow
Write-Host ""

python api.py
