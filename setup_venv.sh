#!/bin/bash
# Skrypt do tworzenia wirtualnego środowiska dla projektu HackNation

echo "========================================"
echo "Tworzenie wirtualnego środowiska"
echo "========================================"

# Sprawdź czy Python jest dostępny
if ! command -v python3 &> /dev/null; then
    echo "BŁĄD: Python3 nie jest zainstalowany"
    exit 1
fi

# Utwórz wirtualne środowisko
echo "[1/3] Tworzenie wirtualnego środowiska..."
python3 -m venv venv

if [ $? -ne 0 ]; then
    echo "BŁĄD: Nie można utworzyć wirtualnego środowiska"
    exit 1
fi

# Aktywuj środowisko
echo "[2/3] Aktywacja środowiska..."
source venv/bin/activate

# Zaktualizuj pip
echo "[3/3] Aktualizacja pip..."
pip install --upgrade pip

# Zainstaluj wymagania dla asystenta (Foreground IP)
echo ""
echo "========================================"
echo "Instalacja wymagań dla Asystenta AI"
echo "========================================"
cd AIWSLUZBIE
pip install -r requirements.txt
cd ..

# Opcjonalnie: Zainstaluj wymagania dla GQPA (Background IP)
echo ""
echo "========================================"
echo "Instalacja wymagań dla GQPA Core (opcjonalne)"
echo "========================================"
read -p "Czy chcesz zainstalować wymagania dla GQPA Core? (t/n): " install_gqpa
if [ "$install_gqpa" = "t" ] || [ "$install_gqpa" = "T" ]; then
    cd gqpa_core
    pip install -r requirements.txt
    cd ..
fi

echo ""
echo "========================================"
echo "✅ ŚRODOWISKO GOTOWE!"
echo "========================================"
echo ""
echo "Aby aktywować środowisko w przyszłości:"
echo "  source venv/bin/activate"
echo ""
echo "Aby dezaktywować:"
echo "  deactivate"
echo ""

