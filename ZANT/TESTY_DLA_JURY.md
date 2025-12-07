# 🧪 Przewodnik Testowy dla Jury

## Jak Przetestować ZANT

### Opcja 1: Użyj Gotowego Frontendu (Najłatwiejsze)

1. **Uruchom backend:**
```bash
cd ZANT/backend
python -m api.main
```

2. **Otwórz frontend:**
   - Otwórz plik `ZANT/frontend/index.html` w przeglądarce
   - LUB użyj serwera: `cd ZANT/frontend && python -m http.server 3000`

3. **Test Asystenta Zgłoszenia:**
   - Przejdź do zakładki "Asystent Zgłoszenia"
   - Wypełnij tylko pole "Okoliczności wypadku" (np. "Spadłem z drabiny")
   - Kliknij "Analizuj Zgłoszenie"
   - Zobaczysz brakujące pola i sugestie

4. **Test Wsparcia Decyzji:**
   - Przejdź do zakładki "Wsparcie Decyzji"
   - Przeciągnij plik PDF z dokumentacją wypadku
   - Poczekaj na analizę (10-30 sekund)
   - Zobaczysz rekomendację decyzji

---

### Opcja 2: Użyj API Bezpośrednio (Dla Zaawansowanych)

#### Test 1: Analiza Zgłoszenia

```bash
curl -X POST "http://localhost:8000/api/report/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "okolicznosci_wypadku": "W trakcie pracy na drabinie, poślizgnąłem się i spadłem.",
    "opis_urazu": "Złamanie ręki"
  }'
```

**Oczekiwany wynik:**
- `completeness_score` < 1.0 (niekompletne)
- Lista `missing_fields` z sugestiami
- `suggestions` z rekomendacjami

#### Test 2: Pełne Zgłoszenie

```bash
curl -X POST "http://localhost:8000/api/report/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "data_wypadku": "2024-12-07",
    "godzina_wypadku": "14:30",
    "miejsce_wypadku": "ul. Przykładowa 123, Warszawa",
    "okolicznosci_wypadku": "W trakcie pracy na drabinie, poślizgnąłem się i spadłem z wysokości 2 metrów.",
    "przyczyna_wypadku": "Poślizgnięcie na mokrej podłodze",
    "dane_poszkodowanego": "Jan Kowalski, PESEL: 12345678901",
    "rodzaj_dzialalnosci": "Remonty",
    "opis_urazu": "Złamanie lewej ręki"
  }'
```

**Oczekiwany wynik:**
- `completeness_score` = 1.0 (kompletne)
- `missing_fields` = [] (brak brakujących pól)
- `suggestions` z pozytywnymi komentarzami

#### Test 3: Analiza Dokumentacji PDF

```bash
curl -X POST "http://localhost:8000/api/decision/analyze" \
  -F "file=@przyklad_karty_wypadku.pdf"
```

**Oczekiwany wynik:**
- `decision`: "recognize", "not_recognize", lub "needs_review"
- `confidence`: 0.0 - 1.0
- `reasoning`: szczegółowe uzasadnienie
- `legal_basis`: lista podstaw prawnych
- `risk_factors`: lista czynników ryzyka

---

## Przykładowe Pliki Testowe

### Test Case 1: Typowy Wypadek przy Pracy

**Dane:**
- Data: 2024-12-07, 14:30
- Miejsce: Budowa, ul. Przykładowa 123
- Okoliczności: Spadek z rusztowania z wysokości 3m podczas malowania
- Przyczyna: Zerwanie liny zabezpieczającej
- Uraz: Złamanie nogi, wstrząs mózgu

**Oczekiwany wynik:** ✅ UZNAĆ (wysoka pewność)

### Test Case 2: Wypadek w Drodze do Pracy

**Dane:**
- Okoliczności: Wypadek samochodowy w drodze do pracy
- Brak związku z pracą

**Oczekiwany wynik:** ❌ NIE UZNAWAĆ (brak związku z pracą)

### Test Case 3: Niekompletne Zgłoszenie

**Dane:**
- Tylko: "Spadłem z drabiny"

**Oczekiwany wynik:**
- Wykrycie 7 brakujących pól
- Sugestie uzupełnień dla każdego pola

---

## Kryteria Oceny

### 1. Związek z Wyzwaniem (10%)
- ✅ System rozwiązuje problem ZUS
- ✅ Wspiera obywateli w zgłaszaniu wypadków
- ✅ Wspiera pracowników ZUS w decyzjach

### 2. Pomysł (10%)
- ✅ Inteligentny asystent zamiast prostego formularza
- ✅ Wykorzystanie AI do analizy dokumentacji
- ✅ Proste, dostępne interfejsy

### 3. Oryginalność (20%)
- ✅ Wykorzystanie HAMA Diamond (unikalne podejście)
- ✅ Kombinacja reasoning + reguły decyzyjne
- ✅ Inteligentna analiza zamiast prostych reguł

### 4. Potencjał Wdrożeniowy (20%)
- ✅ Gotowe do wdrożenia (lub blisko)
- ✅ Skalowalna architektura (FastAPI)
- ✅ Dokumentacja wdrożenia
- ✅ Plan rozwoju

### 5. Jakość Odpowiedzi (40%)
- ✅ Poprawne wykrywanie brakujących pól
- ✅ Trafne rekomendacje decyzji
- ✅ Szczegółowe uzasadnienia
- ✅ Wysoka pewność decyzji

---

## Checklist dla Jury

### Podstawowe Funkcjonalności:
- [ ] Asystent analizuje zgłoszenie
- [ ] Wykrywa brakujące pola
- [ ] Generuje sugestie uzupełnień
- [ ] Analizuje dokumentację PDF
- [ ] Rekomenduje decyzję
- [ ] Generuje uzasadnienie

### Jakość:
- [ ] Sugestie są pomocne i zrozumiałe
- [ ] Rekomendacje są trafne
- [ ] Uzasadnienia są szczegółowe
- [ ] System działa szybko (< 30 sekund)

### UX/UI:
- [ ] Interfejs jest intuicyjny
- [ ] Formularz jest łatwy do wypełnienia
- [ ] Wyniki są czytelne
- [ ] System jest dostępny (prosty język)

### Dokumentacja:
- [ ] README jest kompletny
- [ ] Instrukcje są jasne
- [ ] Architektura jest opisana
- [ ] Plan wdrożenia jest realistyczny

---

## Kontakt w Rzeczywistości Hackathonu

Jeśli masz pytania lub problemy:
1. Sprawdź `QUICK_START.md` - szybki start
2. Sprawdź `INSTALACJA.md` - rozwiązanie problemów
3. Sprawdź `PRZYKLAD_UZYCIA.md` - przykłady

---

## Podsumowanie

**ZANT jest gotowy do testów!**

System powinien:
- ✅ Działać od razu po uruchomieniu
- ✅ Analizować zgłoszenia poprawnie
- ✅ Rekomendować decyzje trafnie
- ✅ Być łatwy w użyciu

**Powodzenia w testowaniu! 🚀**

