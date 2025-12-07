#!/bin/bash
# 📦 ZANT - Instalacja środowiska (Linux/Mac)

echo ""
echo "============================================================"
echo "📦 ZANT - INSTALACJA ŚRODOWISKA"
echo "============================================================"
echo ""

# Sprawdź Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python nie jest zainstalowany!"
    echo "Zainstaluj Python 3.10+ z https://www.python.org/"
    exit 1
fi

echo "✅ Python wykryty"
python3 --version
echo ""

# Sprawdź Google API Key
if [ -z "$GOOGLE_API_KEY" ]; then
    echo "⚠️  UWAGA: GOOGLE_API_KEY nie jest ustawione"
    echo ""
    echo "Ustaw zmienną środowiskową przed uruchomieniem:"
    echo "  export GOOGLE_API_KEY=twój_klucz"
    echo ""
    echo "LUB utwórz plik .env z:"
    echo "  GOOGLE_API_KEY=twój_klucz"
    echo ""
    echo "Uzyskaj klucz na: https://aistudio.google.com/"
    echo ""
fi
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
echo "  cd backend"
echo "  python -m api.main"
echo ""

