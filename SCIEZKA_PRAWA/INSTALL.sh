#!/bin/bash
# 📦 SCIEZKA_PRAWA - Instalacja środowiska (Linux/Mac)

echo ""
echo "============================================================"
echo "📦 ŚCIEŻKA PRAWA - INSTALACJA ŚRODOWISKA"
echo "============================================================"
echo ""

# Sprawdź Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python nie jest zainstalowany!"
    echo "Zainstaluj Python 3.9+ z https://www.python.org/"
    exit 1
fi

echo "✅ Python wykryty"
python3 --version
echo ""

# Utwórz venv jeśli nie istnieje
if [ ! -d "venv" ]; then
    echo "[1/3] Tworzenie środowiska wirtualnego..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "❌ Nie udało się utworzyć venv"
        exit 1
    fi
    echo "✅ Venv utworzone"
else
    echo "✅ Venv już istnieje"
fi
echo ""

# Aktywuj venv
echo "[2/3] Aktywacja środowiska..."
source venv/bin/activate
echo "✅ Środowisko aktywowane"
echo ""

# Zainstaluj wymagania
echo "[3/3] Instalowanie zależności..."
pip install --upgrade pip
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "❌ Nie udało się zainstalować zależności"
    exit 1
fi
echo ""

echo "============================================================"
echo "✅ INSTALACJA ZAKOŃCZONA POMYŚLNIE!"
echo "============================================================"
echo ""
echo "Aby uruchomić projekt:"
echo "  source venv/bin/activate"
echo "  python api.py"
echo ""

