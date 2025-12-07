# 🐍 Wirtualne Środowisko Python (venv)

## Szybki start

### Windows

1. **Utwórz i aktywuj venv:**
   ```cmd
   setup_venv.bat
   ```
   
   To automatycznie:
   - Utworzy wirtualne środowisko
   - Zainstaluje wszystkie zależności
   - Aktywuje środowisko

2. **Lub ręcznie:**
   ```cmd
   python -m venv venv
   venv\Scripts\activate.bat
   python -m pip install -r requirements.txt
   ```

3. **Aktywacja w przyszłości:**
   ```cmd
   venv\Scripts\activate.bat
   ```

### Linux/Mac

1. **Utwórz i aktywuj venv:**
   ```bash
   chmod +x setup_venv.sh
   ./setup_venv.sh
   ```

2. **Lub ręcznie:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Aktywacja w przyszłości:**
   ```bash
   source venv/bin/activate
   ```

## Dezaktywacja

Aby wyjść z wirtualnego środowiska:
```bash
deactivate
```

## Dlaczego venv?

- **Izolacja zależności** - nie miesza pakietów z globalnym Pythonem
- **Łatwe zarządzanie** - każdy projekt ma swoje pakiety
- **Czystość systemu** - nie zaśmieca globalnego środowiska
- **Reprodukowalność** - łatwe odtworzenie środowiska na innych maszynach

## Uruchomienie z venv

Po aktywacji venv, uruchom system normalnie:

```bash
python run_demo.py
```

## Aktualizacja zależności

Jeśli dodałeś nowe pakiety do `requirements.txt`:

```bash
# Aktywuj venv
venv\Scripts\activate.bat  # Windows
# lub
source venv/bin/activate  # Linux/Mac

# Zainstaluj nowe zależności
pip install -r requirements.txt
```

## Usunięcie venv

Jeśli chcesz usunąć wirtualne środowisko:

**Windows:**
```cmd
rmdir /s venv
```

**Linux/Mac:**
```bash
rm -rf venv
```

