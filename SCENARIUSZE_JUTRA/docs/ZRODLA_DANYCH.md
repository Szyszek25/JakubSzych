# 📥 Źródła Danych - Scenariusze Jutra

## Przegląd Źródeł

System wykorzystuje **różnorodne źródła danych** do generowania scenariuszy rozwojowych:

1. **Źródła geopolityczne** - Raporty, analizy, newsy
2. **Źródła ekonomiczne** - Dane makroekonomiczne, prognozy
3. **Źródła społeczne** - Badania, trendy, analizy
4. **Źródła bezpieczeństwa** - Raporty bezpieczeństwa, analizy konfliktów

---

## 1. Źródła Geopolityczne

### Raporty MSZ

- **Format**: PDF, DOCX, HTML
- **Częstotliwość**: Ciągła
- **Zawartość**:
  - Analizy sytuacji międzynarodowej
  - Raporty z misji dyplomatycznych
  - Oceny relacji bilateralnych
  - Prognozy geopolityczne

**Jak pobrać:**
- Strona MSZ: https://www.gov.pl/web/dyplomacja
- API MSZ (jeśli dostępne)
- Pliki udostępnione przez organizatorów

---

### Think Tanks i Instytuty

**Źródła:**
- **PISM** (Polski Instytut Spraw Międzynarodowych)
- **OSW** (Ośrodek Studiów Wschodnich)
- **CSIS** (Center for Strategic and International Studies)
- **Chatham House**
- **Brookings Institution**

**Format**: PDF, HTML, RSS
**Częstotliwość**: Tygodniowa/miesięczna

---

### Organizacje Międzynarodowe

**Źródła:**
- **ONZ** - Raporty i rezolucje
- **UE** - Komunikaty i analizy
- **NATO** - Raporty bezpieczeństwa
- **OECD** - Analizy ekonomiczne
- **Bank Światowy** - Prognozy gospodarcze

**Format**: PDF, JSON, XML
**Częstotliwość**: Różna

---

## 2. Źródła Ekonomiczne

### Dane Makroekonomiczne

**Źródła:**
- **GUS** (Główny Urząd Statystyczny)
- **NBP** (Narodowy Bank Polski)
- **Eurostat**
- **IMF** (Międzynarodowy Fundusz Walutowy)
- **World Bank**

**Dane:**
- PKB i wzrost gospodarczy
- Inflacja
- Bezrobocie
- Handel zagraniczny
- Inwestycje

**Format**: CSV, Excel, JSON
**Częstotliwość**: Miesięczna/kwartalna

---

### Prognozy Ekonomiczne

**Źródła:**
- **IMF World Economic Outlook**
- **OECD Economic Outlook**
- **NBP Raport o inflacji**
- **Komisja Europejska - Prognozy**

**Format**: PDF, Excel
**Częstotliwość**: Kwartalna

---

## 3. Źródła Społeczne

### Badania Opinii Publicznej

**Źródła:**
- **CBOS** (Centrum Badania Opinii Społecznej)
- **Pew Research Center**
- **Eurobarometer**

**Dane:**
- Nastroje społeczne
- Zaufanie do instytucji
- Priorytety społeczne
- Postawy wobec polityki

**Format**: PDF, CSV
**Częstotliwość**: Miesięczna/kwartalna

---

### Trendy Społeczne

**Źródła:**
- **Google Trends**
- **Twitter/X Analytics**
- **Facebook Insights**
- **LinkedIn Analytics**

**Dane:**
- Trendy wyszukiwań
- Tematy dyskusji
- Nastroje w mediach społecznościowych

**Format**: JSON, CSV
**Częstotliwość**: Ciągła

---

## 4. Źródła Bezpieczeństwa

### Raporty Bezpieczeństwa

**Źródła:**
- **NATO** - Raporty bezpieczeństwa
- **EU** - Raporty bezpieczeństwa
- **RAND Corporation**
- **IISS** (International Institute for Strategic Studies)

**Dane:**
- Analizy konfliktów
- Oceny zagrożeń
- Prognozy bezpieczeństwa
- Analizy wojskowe

**Format**: PDF, HTML
**Częstotliwość**: Miesięczna/kwartalna

---

## 5. Media i Newsy

### Agencje Informacyjne

**Źródła:**
- **Reuters**
- **AP** (Associated Press)
- **AFP** (Agence France-Presse)
- **Bloomberg**
- **Financial Times**

**Format**: RSS, JSON, HTML
**Częstotliwość**: Ciągła

---

### Media Specjalistyczne

**Źródła:**
- **Foreign Policy**
- **The Economist**
- **Financial Times**
- **Wall Street Journal**

**Format**: RSS, HTML
**Częstotliwość**: Tygodniowa/dzienna

---

## Metody Pobierania Danych

### 1. API

**Gdy dostępne:**
- REST API
- GraphQL API
- Webhooks

**Przykłady:**
- Twitter API
- Google Trends API
- News API

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

### 1. Normalizacja

- Standaryzacja formatów
- Konwersja jednostek
- Ujednolicenie kodowań

### 2. Weryfikacja

- Sprawdzanie kompletności
- Wykrywanie błędów
- Walidacja danych

### 3. Enrichment

- Dodawanie metadanych
- Tagowanie
- Klasyfikacja

---

## Przechowywanie Danych

### Struktura Folderów

```
data/
├── raw/              # Surowe dane
│   ├── geopolitics/
│   ├── economics/
│   ├── social/
│   └── security/
├── processed/        # Przetworzone dane
│   ├── facts/
│   ├── trends/
│   └── scenarios/
└── cache/            # Cache
```

---

## Aktualizacja Danych

### Częstotliwość

- **Ciągła** - Media, newsy
- **Dzienna** - Raporty, analizy
- **Tygodniowa** - Badania, trendy
- **Miesięczna** - Dane statystyczne
- **Kwartalna** - Prognozy

### Automatyzacja

- **Scheduled tasks** - Automatyczne pobieranie
- **Webhooks** - Reakcja na zmiany
- **Monitoring** - Wykrywanie nowych danych

---

## Jakość Danych

### Metryki

- **Aktualność** - Świeżość danych
- **Kompletność** - Pokrycie wszystkich obszarów
- **Dokładność** - Poprawność danych
- **Wierygodność** - Rzetelność źródeł

### Weryfikacja

- **Cross-reference** - Porównanie z innymi źródłami
- **Expert review** - Przegląd ekspercki
- **Validation** - Walidacja logiczna

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

System **Scenariusze Jutra** wykorzystuje **różnorodne źródła danych** do generowania wiarygodnych scenariuszy rozwojowych. Kluczowe jest:

- **Różnorodność** źródeł
- **Aktualność** danych
- **Wiarygodność** źródeł
- **Kompletność** pokrycia
- **Jakość** przetwarzania


