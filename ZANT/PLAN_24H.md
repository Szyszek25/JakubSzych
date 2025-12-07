# ⏰ Plan Pracy - 24h Hackathon

## Faza 1: Setup i Podstawowa Struktura (2h)

- [x] Stworzenie struktury projektu
- [x] Konfiguracja środowiska
- [x] Podstawowe modele danych
- [x] FastAPI skeleton

**Czas: 2h**

## Faza 2: Asystent Zgłoszenia (4h)

- [x] Implementacja `AccidentAssistant`
- [x] Integracja z HAMA/Gemini
- [x] Wykrywanie brakujących pól
- [x] Generowanie sugestii
- [x] API endpoint `/api/report/analyze`

**Czas: 4h**

## Faza 3: Ekstrakcja PDF (3h)

- [x] Implementacja `PDFExtractor`
- [x] Obsługa tekstowych PDF
- [x] Integracja OCR (Tesseract)
- [x] Ekstrakcja strukturalnych danych

**Czas: 3h**

## Faza 4: Silnik Decyzyjny (4h)

- [x] Implementacja `DecisionEngine`
- [x] Integracja z HAMA Diamond do analizy
- [x] Reguły decyzyjne ZUS
- [x] Generowanie rekomendacji
- [x] Generator karty wypadku
- [x] API endpoint `/api/decision/analyze`

**Czas: 4h**

## Faza 5: Frontend (3h)

- [x] HTML/CSS/JS interface
- [x] Formularz zgłoszenia
- [x] Upload PDF
- [x] Wyświetlanie wyników
- [x] Integracja z API

**Czas: 3h**

## Faza 6: Testowanie i Debugowanie (3h)

- [ ] Testy z przykładowymi danymi
- [ ] Testy z prawdziwymi kartami wypadków
- [ ] Poprawki błędów
- [ ] Optymalizacja promptów
- [ ] Ulepszenie UI/UX

**Czas: 3h**

## Faza 7: Dokumentacja i Prezentacja (2h)

- [x] README
- [x] Dokumentacja architektury
- [x] Instrukcje instalacji
- [ ] Przygotowanie prezentacji
- [ ] Demo video/screenshots

**Czas: 2h**

## Faza 8: Bonus - Ulepszenia (3h)

- [ ] Lepsze OCR (PaddleOCR)
- [ ] Więcej reguł decyzyjnych
- [ ] Dashboard statystyk
- [ ] Eksport do PDF
- [ ] Integracja z bazą precedensów

**Czas: 3h (opcjonalnie)**

---

## ⚠️ Najważniejsze Punkty

1. **Priorytet 1**: Asystent zgłoszenia musi działać
2. **Priorytet 2**: Analiza PDF i rekomendacja decyzji
3. **Priorytet 3**: Frontend - prosty ale funkcjonalny
4. **Priorytet 4**: Dokumentacja dla jury

## 🎯 Cel Minimum (MVP)

- ✅ Asystent analizuje zgłoszenie i wykrywa braki
- ✅ System analizuje PDF i rekomenduje decyzję
- ✅ Frontend pozwala przetestować obie funkcjonalności
- ✅ Dokumentacja wyjaśnia jak używać

## 🚀 Cel Optymalny

- ✅ Wysoka jakość analizy (HAMA Diamond)
- ✅ Piękny, intuicyjny frontend
- ✅ Działa z prawdziwymi danymi ZUS
- ✅ Gotowe do wdrożenia (lub blisko)

---

## 📝 Notatki

- **Gemini API może być wolne przy pierwszym wywołaniu** - to normalne, cache pomaga
- **OCR może być wolne** - zoptymalizuj lub użyj cache
- **Frontend prosty** - lepiej działający prosty niż skomplikowany nie działający
- **Testuj często** - nie czekaj do końca

