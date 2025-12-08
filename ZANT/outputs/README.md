# 📊 Outputs - HAMA-ZANT

Ten folder zawiera wyniki działania systemu ZANT.

## Struktura

```
outputs/
├── raporty/          # Raporty analiz zgłoszeń
├── karty_wypadkow/   # Wygenerowane karty wypadków
└── wykresy/          # Wizualizacje (jeśli dodane)
```

## Raporty

Raporty są generowane automatycznie podczas analizy zgłoszeń i zawierają:
- Analizę kompletności zgłoszenia
- Wykryte brakujące pola
- Sugestie uzupełnień
- Walidację zgodności

## Karty Wypadków

Karty wypadków są generowane przez Decision Engine i zawierają:
- Rekomendację decyzji
- Uzasadnienie
- Analizę warunków
- Podstawy prawne
- Czynniki ryzyka

## Format

- **Raporty**: Markdown (.md)
- **Karty**: JSON + Markdown
- **Wykresy**: HTML (jeśli dodane)

---

*Folder jest tworzony automatycznie podczas działania systemu.*


