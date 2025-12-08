# 📝 Przykłady Użycia ZANT

## Przykład 1: Analiza Zgłoszenia (cURL)

```bash
curl -X POST "http://localhost:8000/api/report/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "okolicznosci_wypadku": "W trakcie pracy na drabinie, poślizgnąłem się i spadłem z wysokości około 2 metrów.",
    "opis_urazu": "Złamanie lewej ręki, stłuczenia"
  }'
```

### Odpowiedź:

```json
{
  "report_id": "RPT-abc123",
  "completeness_score": 0.25,
  "missing_fields": [
    {
      "field_name": "data_wypadku",
      "field_description": "Data zdarzenia (format: YYYY-MM-DD)",
      "priority": "high",
      "suggestion": "Proszę podać dokładną datę wypadku w formacie YYYY-MM-DD, np. 2024-12-07"
    },
    {
      "field_name": "miejsce_wypadku",
      "field_description": "Szczegółowy adres lub lokalizacja wypadku",
      "priority": "high",
      "suggestion": "Proszę podać dokładny adres lub lokalizację wypadku, np. ul. Przykładowa 123, Warszawa"
    }
  ],
  "suggestions": [
    "Opis okoliczności jest dobry, ale warto dodać więcej szczegółów o warunkach pracy",
    "Rozważ dodanie informacji o przyczynie poślizgnięcia"
  ],
  "validation_errors": [],
  "confidence": 0.85
}
```

---

## Przykład 2: Pełne Zgłoszenie

```bash
curl -X POST "http://localhost:8000/api/report/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "data_wypadku": "2024-12-07",
    "godzina_wypadku": "14:30",
    "miejsce_wypadku": "ul. Przykładowa 123, Warszawa",
    "okolicznosci_wypadku": "W trakcie pracy na drabinie, poślizgnąłem się i spadłem z wysokości około 2 metrów. Drabina była niestabilna, a podłoga była mokra po wcześniejszym sprzątaniu.",
    "przyczyna_wypadku": "Poślizgnięcie się na mokrej podłodze podczas pracy na niestabilnej drabinie",
    "dane_poszkodowanego": "Jan Kowalski, PESEL: 12345678901",
    "rodzaj_dzialalnosci": "Remonty i naprawy",
    "opis_urazu": "Złamanie lewej ręki w nadgarstku, stłuczenia prawego kolana"
  }'
```

### Odpowiedź:

```json
{
  "report_id": "RPT-abc123",
  "completeness_score": 1.0,
  "missing_fields": [],
  "suggestions": [
    "Zgłoszenie jest kompletne i szczegółowe",
    "Wszystkie wymagane pola są wypełnione poprawnie"
  ],
  "validation_errors": [],
  "confidence": 0.95
}
```

---

## Przykład 3: Analiza Dokumentacji PDF (Python)

```python
import requests

# Upload pliku PDF
with open("karta_wypadku.pdf", "rb") as f:
    files = {"file": f}
    response = requests.post(
        "http://localhost:8000/api/decision/analyze",
        files=files
    )

result = response.json()
print(f"Rekomendacja: {result['decision']}")
print(f"Pewność: {result['confidence'] * 100}%")
print(f"Uzasadnienie: {result['reasoning']}")
```

### Odpowiedź:

```json
{
  "card_id": "CARD-RPT-abc123-1234567890",
  "report_id": "RPT-abc123",
  "decision": "recognize",
  "confidence": 0.87,
  "reasoning": "Wszystkie warunki definicji wypadku są spełnione. Zdarzenie było nagłe (spadek z drabiny), przyczyna zewnętrzna (mokra podłoga, niestabilna drabina), uraz został udokumentowany (złamanie ręki), a zdarzenie było bezpośrednio związane z pracą (remont).",
  "legal_basis": [
    "Ustawa z dnia 30 października 2002 r. o ubezpieczeniu społecznym z tytułu wypadków przy pracy i chorób zawodowych"
  ],
  "risk_factors": [],
  "extracted_data": {
    "data_wypadku": "2024-12-07",
    "godzina_wypadku": "14:30",
    "miejsce_wypadku": "ul. Przykładowa 123, Warszawa",
    "full_text": "..."
  }
}
```

---

## Przykład 4: JavaScript (Frontend)

```javascript
// Analiza zgłoszenia
async function analyzeReport() {
  const formData = {
    data_wypadku: document.getElementById('data_wypadku').value,
    godzina_wypadku: document.getElementById('godzina_wypadku').value,
    miejsce_wypadku: document.getElementById('miejsce_wypadku').value,
    okolicznosci_wypadku: document.getElementById('okolicznosci_wypadku').value,
    przyczyna_wypadku: document.getElementById('przyczyna_wypadku').value,
    dane_poszkodowanego: document.getElementById('dane_poszkodowanego').value,
    rodzaj_dzialalnosci: document.getElementById('rodzaj_dzialalnosci').value,
    opis_urazu: document.getElementById('opis_urazu').value
  };
  
  const response = await fetch('http://localhost:8000/api/report/analyze', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(formData)
  });
  
  const result = await response.json();
  
  // Wyświetl wyniki
  console.log('Kompletność:', result.completeness_score * 100 + '%');
  console.log('Brakujące pola:', result.missing_fields);
  console.log('Sugestie:', result.suggestions);
}

// Analiza dokumentacji
async function analyzeDecision(file) {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await fetch('http://localhost:8000/api/decision/analyze', {
    method: 'POST',
    body: formData
  });
  
  const result = await response.json();
  
  // Wyświetl wyniki
  console.log('Rekomendacja:', result.decision);
  console.log('Pewność:', result.confidence * 100 + '%');
  console.log('Uzasadnienie:', result.reasoning);
}
```

---

## Przykład 5: Scenariusz Testowy

### Scenariusz: Wypadek przy pracy na wysokości

**Dane wejściowe:**
- Data: 2024-12-07
- Godzina: 14:30
- Miejsce: Budowa, ul. Przykładowa 123, Warszawa
- Okoliczności: Pracownik spadł z rusztowania z wysokości 3 metrów podczas malowania elewacji
- Przyczyna: Zerwanie się liny zabezpieczającej
- Uraz: Złamanie nogi, wstrząs mózgu

**Oczekiwany wynik:**
- ✅ UZNAĆ ZA WYPADEK
- Pewność: > 80%
- Wszystkie warunki spełnione

### Scenariusz: Wypadek w drodze do pracy

**Dane wejściowe:**
- Okoliczności: Wypadek samochodowy w drodze do pracy
- Brak związku z pracą

**Oczekiwany wynik:**
- ❌ NIE UZNAWAĆ ZA WYPADEK
- Uzasadnienie: Brak związku z pracą (wypadek w drodze do pracy)

---

## Testowanie z Prawdziwymi Danymi ZUS

1. **Przygotuj dane testowe:**
   - Pobierz przykładowe karty wypadków od ZUS
   - Zapisz jako PDF w folderze `data/`

2. **Uruchom testy:**
```python
import os
from backend.services.pdf_extractor import PDFExtractor
from backend.services.decision_engine import DecisionEngine

extractor = PDFExtractor()
engine = DecisionEngine()

# Test dla każdego pliku
for pdf_file in os.listdir("data/"):
    if pdf_file.endswith(".pdf"):
        extraction = extractor.extract_from_pdf(f"data/{pdf_file}")
        card = engine.analyze_and_recommend(extraction, f"RPT-{pdf_file}")
        
        print(f"Plik: {pdf_file}")
        print(f"Decyzja: {card.decision.value}")
        print(f"Pewność: {card.confidence * 100:.1f}%")
        print(f"Uzasadnienie: {card.reasoning}")
        print("-" * 50)
```

3. **Porównaj z rzeczywistymi decyzjami ZUS:**
   - Sprawdź zgodność rekomendacji
   - Oceń jakość uzasadnień
   - Zidentyfikuj obszary do poprawy


