#!/bin/bash

echo "========================================"
echo "Tworzenie wirtualnego środowiska Python"
echo "========================================"
echo ""

cd "$(dirname "$0")"

# Sprawdzenie czy venv już istnieje
if [ -d "venv" ]; then
    echo "Wirtualne środowisko już istnieje!"
    echo ""
    echo "Aby aktywować: source venv/bin/activate"
    echo "Aby dezaktywować: deactivate"
    exit 0
fi

echo "Tworzenie wirtualnego środowiska..."
python3 -m venv venv

if [ $? -ne 0 ]; then
    echo "BŁĄD: Nie udało się utworzyć wirtualnego środowiska!"
    echo "Sprawdź czy Python3 jest zainstalowany."
    exit 1
fi

echo ""
echo "Aktywowanie wirtualnego środowiska..."
source venv/bin/activate

echo ""
echo "Aktualizacja pip..."
python -m pip install --upgrade pip

echo ""
echo "Instalowanie zależności z requirements.txt..."
python -m pip install -r requirements.txt

echo ""
echo "========================================"
echo "Wirtualne środowisko utworzone!"
echo "========================================"
echo ""
echo "Aby aktywować w przyszłości:"
echo "  source venv/bin/activate"
echo ""
echo "Aby dezaktywować:"
echo "  deactivate"
echo ""

