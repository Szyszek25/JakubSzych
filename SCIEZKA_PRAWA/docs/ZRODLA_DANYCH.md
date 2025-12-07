# 📥 Źródła Danych - Ścieżka Prawa (GQPA Legislative Navigator)

## Przegląd Źródeł

System wykorzystuje **różnorodne źródła danych** do monitorowania i analizy procesów legislacyjnych:

1. **Rządowe Centrum Legislacji (RCL)** - Projekty aktów prawnych
2. **Sejm** - Projekty ustaw, uchwały
3. **Senat** - Uchwały senatu, poprawki
4. **Biuletyn Informacji Publicznej (BIP)** - Dokumenty urzędowe
5. **Konsultacje społeczne** - Uwagi i komentarze obywateli

---

## 1. Rządowe Centrum Legislacji (RCL)

### Dostępne dane:

- **Projekty aktów prawnych** (ustawy, rozporządzenia)
  - Format: HTML, PDF, DOCX
  - Częstotliwość: Ciągła
  - Poziom: Pełne teksty projektów

- **Konsultacje społeczne**
  - Format: HTML, PDF
  - Częstotliwość: Ciągła
  - Poziom: Dokumenty konsultacyjne

- **Metadane**
  - Autor projektu
  - Data publikacji
  - Status
  - Historia zmian

### Jak pobrać:

1. Wejdź na https://www.gov.pl/web/rcl
2. Przejdź do sekcji "Projekty aktów prawnych"
3. Pobierz dokumenty lub użyj API (jeśli dostępne)

### Alternatywa:

- **API RCL** (jeśli dostępne)
- **RSS feeds** - Subskrypcja nowych projektów
- **Pliki udostępnione przez organizatorów hackathonu**

---

## 2. Sejm (sejm.gov.pl)

### Dostępne dane:

- **Projekty ustaw**
  - Format: HTML, PDF
  - Częstotliwość: Ciągła
  - Poziom: Pełne teksty projektów

- **Uchwały Sejmu**
  - Format: HTML, PDF
  - Częstotliwość: Ciągła
  - Poziom: Pełne teksty uchwał

- **Sprawozdania komisji**
  - Format: PDF, HTML
  - Częstotliwość: Ciągła
  - Poziom: Pełne sprawozdania

- **Głosowania**
  - Format: JSON, XML
  - Częstotliwość: Ciągła
  - Poziom: Wyniki głosowań

### Jak pobrać:

1. Wejdź na https://www.sejm.gov.pl
2. Przejdź do sekcji "Druki sejmowe"
3. Pobierz dokumenty lub użyj API

### Alternatywa:

- **API Sejmu** (jeśli dostępne)
- **RSS feeds**
- **Web scraping**

---

## 3. Senat (senat.gov.pl)

### Dostępne dane:

- **Uchwały Senatu**
  - Format: HTML, PDF
  - Częstotliwość: Ciągła
  - Poziom: Pełne teksty uchwał

- **Poprawki Senatu**
  - Format: HTML, PDF
  - Częstotliwość: Ciągła
  - Poziom: Pełne teksty poprawek

- **Sprawozdania komisji**
  - Format: PDF, HTML
  - Częstotliwość: Ciągła
  - Poziom: Pełne sprawozdania

### Jak pobrać:

1. Wejdź na https://www.senat.gov.pl
2. Przejdź do sekcji "Druki senackie"
3. Pobierz dokumenty

---

## 4. Biuletyn Informacji Publicznej (BIP)

### Dostępne dane:

- **Dokumenty urzędowe**
  - Format: HTML, PDF, DOCX
  - Częstotliwość: Ciągła
  - Poziom: Różne

- **Informacje publiczne**
  - Format: HTML, PDF
  - Częstotliwość: Ciągła
  - Poziom: Różne

### Jak pobrać:

1. Wejdź na https://www.bip.gov.pl
2. Przejdź do sekcji odpowiedniej instytucji
3. Pobierz dokumenty

---

## 5. Konsultacje Społeczne

### Dostępne dane:

- **Uwagi obywateli**
  - Format: JSON, HTML
  - Częstotliwość: Ciągła
  - Poziom: Indywidualne uwagi

- **Komentarze**
  - Format: JSON, HTML
  - Częstotliwość: Ciągła
  - Poziom: Indywidualne komentarze

- **Feedback**
  - Format: JSON
  - Częstotliwość: Ciągła
  - Poziom: Oceny i opinie

### Jak pobrać:

- **API systemu** - Endpoint `/api/consultations/{id}/feedback`
- **Baza danych** - Bezpośredni dostęp (jeśli dostępne)
- **Eksport** - Pliki CSV/JSON

---

## Metody Pobierania Danych

### 1. API

**Gdy dostępne:**
- REST API
- GraphQL API
- Webhooks

**Przykłady:**
- API Sejmu
- API RCL
- API BIP

---

### 2. Web Scraping

**Gdy API niedostępne:**
- BeautifulSoup
- Scrapy
- Selenium (dla JS)

**Etyka:**
- Respektowanie robots.txt
- Ograniczenie częstotliwości
- Szanowanie praw autorskich

---

### 3. Pliki

**Gdy API i scraping niemożliwe:**
- Pobieranie ręczne
- Pliki udostępnione przez organizatorów
- Pliki z otwartych źródeł

---

## Przetwarzanie Danych

### 1. Parsing Dokumentów

**Formaty:**
- **PDF** - pdfplumber, PyPDF2
- **DOCX** - python-docx
- **HTML** - BeautifulSoup
- **TXT** - Standardowe czytanie plików

### 2. Ekstrakcja Tekstu

- **OCR** - Dla dokumentów skanowanych (Tesseract)
- **Text extraction** - Dla dokumentów tekstowych
- **Structure detection** - Wykrywanie struktury

### 3. Normalizacja

- Standaryzacja formatów
- Usuwanie formatowania
- Normalizacja encodingu
- Czyszczenie tekstu

### 4. Enrichment

- Dodawanie metadanych
- Tagowanie
- Klasyfikacja
- Entity recognition

---

## Przechowywanie Danych

### Struktura Folderów

```
data/
├── raw/              # Surowe dane
│   ├── rcl/
│   ├── sejm/
│   ├── senat/
│   └── bip/
├── processed/        # Przetworzone dane
│   ├── documents/
│   ├── simplified/
│   └── analyses/
└── cache/            # Cache
```

---

## Aktualizacja Danych

### Częstotliwość

- **Ciągła** - Monitoring nowych dokumentów
- **Dzienna** - Aktualizacja statusów
- **Tygodniowa** - Pełna synchronizacja
- **Na żądanie** - Manual refresh

### Automatyzacja

- **Scheduled tasks** - Automatyczne pobieranie
- **Webhooks** - Reakcja na zmiany
- **Monitoring** - Wykrywanie nowych dokumentów
- **Notifications** - Powiadomienia o zmianach

---

## Jakość Danych

### Metryki

- **Aktualność** - Świeżość danych
- **Kompletność** - Pokrycie wszystkich dokumentów
- **Dokładność** - Poprawność danych
- **Wierygodność** - Rzetelność źródeł

### Weryfikacja

- **Cross-reference** - Porównanie z innymi źródłami
- **Expert review** - Przegląd ekspercki
- **Validation** - Walidacja logiczna
- **Quality checks** - Automatyczne sprawdzanie jakości

---

## Bezpieczeństwo Danych

### Ochrona

- **Szyfrowanie** - Dane wrażliwe
- **Access control** - Kontrola dostępu
- **Backup** - Kopie zapasowe
- **Audit** - Logowanie dostępu

### Compliance

- **RODO** - Ochrona danych osobowych
- **GDPR** - Ogólne rozporządzenie o ochronie danych
- **Prawa autorskie** - Szanowanie praw

---

## Wnioski

System **Ścieżka Prawa** wykorzystuje **różnorodne źródła danych** do monitorowania i analizy procesów legislacyjnych. Kluczowe jest:

- **Różnorodność** źródeł
- **Aktualność** danych
- **Kompletność** pokrycia
- **Jakość** przetwarzania
- **Bezpieczeństwo** danych

