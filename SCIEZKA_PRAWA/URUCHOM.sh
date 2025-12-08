#!/bin/bash

echo "========================================"
echo "  SCIEZKA PRAWA - Uruchomienie API"
echo "========================================"
echo ""

cd "$(dirname "$0")"

# Sprawdź czy Python jest zainstalowany
if ! command -v python3 &> /dev/null; then
    echo "[BŁĄD] Python nie jest zainstalowany!"
    echo "Zainstaluj Python 3.9+ z https://www.python.org/"
    exit 1
fi

# Sprawdź czy venv istnieje
if [ ! -d "venv" ]; then
    echo "[INFO] Tworzenie wirtualnego środowiska..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "[BŁĄD] Nie można utworzyć venv!"
        exit 1
    fi
fi

# Aktywuj venv
echo "[INFO] Aktywacja wirtualnego środowiska..."
source venv/bin/activate

# Zainstaluj zależności
if [ ! -d "venv/lib/python*/site-packages/fastapi" ]; then
    echo "[INFO] Instalacja zależności..."
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "[BŁĄD] Nie można zainstalować zależności!"
        exit 1
    fi
fi

# Uruchom API
echo ""
echo "[INFO] Uruchamianie API..."
echo "[INFO] API będzie dostępne pod: http://localhost:8003"
echo "[INFO] Dokumentacja: http://localhost:8003/docs"
echo ""
echo "Naciśnij Ctrl+C aby zatrzymać serwer"
echo ""

python api.py


