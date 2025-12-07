# 🏛️ Dashboard Asystenta AI dla Administracji

Nowoczesny dashboard React z TypeScript dla systemu Asystenta AI wspierającego orzeczników w Departamencie Turystyki MSiT.

## 🚀 Szybki start

### Wymagania
- Node.js 18+ 
- npm lub yarn
- Backend API działający na porcie 8000

### Instalacja

```bash
cd dashboard-frontend
npm install
```

### Uruchomienie

```bash
npm run dev
```

Dashboard będzie dostępny na: http://localhost:3000

### Build produkcyjny

```bash
npm run build
```

## 📦 Funkcjonalności

- **Statystyki w czasie rzeczywistym** - karty z kluczowymi metrykami
- **Wykresy i wizualizacje** - Recharts do prezentacji danych
- **Lista spraw** - przegląd wszystkich spraw administracyjnych
- **Status systemu** - monitorowanie GQPA, Ollama, Gemini, Guardrails
- **Terminy** - lista zbliżających się terminów z priorytetami
- **Truth Guardian** - statystyki wykrywania dezinformacji (COI)

## 🏗️ Architektura

```
dashboard-frontend/
├── src/
│   ├── components/      # Komponenty React
│   │   ├── Dashboard.tsx
│   │   ├── StatCards.tsx
│   │   ├── ChartsSection.tsx
│   │   ├── CasesList.tsx
│   │   ├── SystemStatusPanel.tsx
│   │   ├── DeadlinesPanel.tsx
│   │   └── TruthGuardianPanel.tsx
│   ├── services/       # API client
│   │   └── api.ts
│   ├── types/          # TypeScript types
│   │   └── types.ts
│   ├── App.tsx         # Główny komponent
│   └── main.tsx        # Entry point
├── package.json
└── vite.config.ts
```

## 🔌 Integracja z Backendem

Dashboard komunikuje się z backendem przez REST API:

- `GET /api/dashboard/stats` - główne statystyki
- `GET /api/cases` - lista spraw
- `GET /api/system/status` - status systemu
- `GET /api/deadlines` - terminy
- `POST /api/cases/{id}/analyze` - analiza sprawy
- `POST /api/cases/{id}/generate-decision` - generowanie decyzji

## 🎨 Technologie

- **React 18** - framework UI
- **TypeScript** - type safety
- **Vite** - build tool
- **Recharts** - wykresy
- **Lucide React** - ikony
- **date-fns** - formatowanie dat

## 📱 Responsywność

Dashboard jest w pełni responsywny i działa na:
- Desktop (1920px+)
- Laptop (1200px+)
- Tablet (768px+)
- Mobile (320px+)

## 🔒 Bezpieczeństwo

- CORS skonfigurowany dla localhost
- Walidacja danych przez TypeScript
- Sanityzacja danych z backendu

