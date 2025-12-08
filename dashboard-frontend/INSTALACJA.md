# 🚀 Instalacja Frontendu - Scenariusze Jutra

## Wymagania

- **Node.js** (wersja 18 lub nowsza)
- **npm** (zazwyczaj dołączony do Node.js)

## 📦 Instalacja

### Krok 1: Przejdź do katalogu frontendu

```powershell
cd dashboard-frontend
```

### Krok 2: Zainstaluj zależności

```powershell
npm install
```

To może zająć kilka minut - npm pobierze wszystkie wymagane pakiety.

## 🎯 Uruchomienie

### Opcja 1: Użyj gotowego skryptu (NAJŁATWIEJ)

```powershell
.\start.bat
```

Skrypt automatycznie:
- Sprawdzi czy `node_modules` istnieje
- Jeśli nie - zainstaluje zależności
- Uruchomi serwer deweloperski

### Opcja 2: Ręcznie

```powershell
npm run dev
```

## 🌐 Dostęp

Po uruchomieniu frontend będzie dostępny na:
- **http://localhost:5173** (Vite domyślnie używa portu 5173)

## ⚙️ Konfiguracja API

Frontend domyślnie łączy się z API na porcie **8001**.

### Jeśli używasz NOWEGO projektu (port 8002):

Utwórz plik `.env` w katalogu `dashboard-frontend`:

```env
VITE_API_URL=http://localhost:8002
```

Lub zmień w `src/services/scenariosApi.ts`:
```typescript
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8002'
```

## 🔧 Rozwiązywanie problemów

### Problem: "npm nie jest rozpoznany"
- Zainstaluj Node.js z: https://nodejs.org/
- Uruchom ponownie terminal

### Problem: "Port 5173 już zajęty"
- Vite automatycznie użyje następnego dostępnego portu (5174, 5175, itd.)
- Sprawdź w terminalu, na którym porcie faktycznie działa

### Problem: "Błąd połączenia z API"
- Upewnij się, że backend API działa (port 8001 lub 8002)
- Sprawdź czy port w `.env` lub `scenariosApi.ts` jest poprawny
- Sprawdź CORS w backendzie

## 📝 Skrypty npm

- `npm run dev` - Uruchom serwer deweloperski
- `npm run build` - Zbuduj wersję produkcyjną
- `npm run preview` - Podgląd wersji produkcyjnej
- `npm run lint` - Sprawdź kod (ESLint)


