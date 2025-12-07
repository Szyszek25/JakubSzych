#!/bin/bash
# Skrypt do tworzenia wirtualnego środowiska dla GQPA Core (Background IP)

echo "========================================"
echo "Tworzenie wirtualnego środowiska GQPA"
echo "========================================"

# Sprawdź czy Python jest dostępny
if ! command -v python3 &> /dev/null; then
    echo "BŁĄD: Python3 nie jest zainstalowany"
    exit 1
fi

# Utwórz wirtualne środowisko
echo "[1/3] Tworzenie wirtualnego środowiska..."
python3 -m venv venv_gqpa

if [ $? -ne 0 ]; then
    echo "BŁĄD: Nie można utworzyć wirtualnego środowiska"
    exit 1
fi

# Aktywuj środowisko
echo "[2/3] Aktywacja środowiska..."
source venv_gqpa/bin/activate

# Zaktualizuj pip
echo "[3/3] Aktualizacja pip..."
pip install --upgrade pip

# Zainstaluj wymagania dla GQPA
echo ""
echo "========================================"
echo "Instalacja wymagań dla GQPA Core"
echo "========================================"
cd gqpa_core
pip install -r requirements.txt
cd ..

echo ""
echo "========================================"
echo "✅ ŚRODOWISKO GQPA GOTOWE!"
echo "========================================"
echo ""
echo "Aby aktywować środowisko w przyszłości:"
echo "  source venv_gqpa/bin/activate"
echo ""
echo "Aby dezaktywować:"
echo "  deactivate"
echo ""

