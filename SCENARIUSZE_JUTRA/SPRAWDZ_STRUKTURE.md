# ✅ Sprawdzenie struktury katalogów

## Prawidłowa struktura:

```
SCENARIUSZE_JUTRA/
├── venv/                    ← Wirtualne środowisko (tutaj!)
├── data_collector.py
├── main_orchestrator.py
├── run_demo.py
├── requirements.txt
└── ... (inne pliki)
```

## ❌ Nieprawidłowa struktura:

```
SCENARIUSZE_JUTRA/
├── SCENARIUSZE_JUTRA/       ← BŁĄD: podwójny katalog!
│   └── venv/
└── venv/                    ← Powinien być tutaj
```

## Jak naprawić:

Jeśli widzisz podwójny katalog `SCENARIUSZE_JUTRA\SCENARIUSZE_JUTRA`:

1. **Usuń podwójny katalog:**
   ```cmd
   rmdir /s SCENARIUSZE_JUTRA\SCENARIUSZE_JUTRA
   ```

2. **Upewnij się, że venv jest w głównym katalogu:**
   ```cmd
   dir SCENARIUSZE_JUTRA\venv
   ```

3. **Jeśli venv nie istnieje, utwórz go:**
   ```cmd
   cd SCENARIUSZE_JUTRA
   python -m venv venv
   venv\Scripts\activate.bat
   pip install -r requirements.txt
   ```

## Sprawdzenie:

Uruchom:
```cmd
cd SCENARIUSZE_JUTRA
dir
```

Powinieneś zobaczyć:
- `venv\` (katalog)
- `data_collector.py`
- `main_orchestrator.py`
- `run_demo.py`
- itd.

**NIE powinieneś widzieć:**
- `SCENARIUSZE_JUTRA\` (podkatalog)

