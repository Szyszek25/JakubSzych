# Kompletny skrypt setup Ollama dla Windows
# Uruchom: .\setup_ollama.ps1

Write-Host "🔧 Konfiguracja Ollama dla HackNation" -ForegroundColor Cyan
Write-Host "=" * 50

# Krok 1: Dodaj do PATH
Write-Host "`n[1/4] Dodawanie Ollama do PATH..." -ForegroundColor Yellow
$ollamaPath = "$env:LOCALAPPDATA\Programs\Ollama"

if (Test-Path "$ollamaPath\ollama.exe") {
    # Dodaj do PATH użytkownika (na stałe)
    $currentPath = [Environment]::GetEnvironmentVariable("Path", "User")
    if ($currentPath -notlike "*$ollamaPath*") {
        [Environment]::SetEnvironmentVariable(
            "Path",
            $currentPath + ";$ollamaPath",
            "User"
        )
        Write-Host "✅ Ollama dodane do PATH" -ForegroundColor Green
    } else {
        Write-Host "✅ Ollama już jest w PATH" -ForegroundColor Green
    }
    
    # Dodaj do PATH bieżącej sesji
    $env:Path += ";$ollamaPath"
} else {
    Write-Host "❌ Ollama nie znaleziono w: $ollamaPath" -ForegroundColor Red
    Write-Host "   Zainstaluj z: https://ollama.ai/download" -ForegroundColor Yellow
    exit 1
}

# Krok 2: Sprawdź wersję
Write-Host "`n[2/4] Sprawdzanie wersji..." -ForegroundColor Yellow
try {
    $version = ollama --version
    Write-Host "✅ $version" -ForegroundColor Green
} catch {
    Write-Host "❌ Błąd: $_" -ForegroundColor Red
    exit 1
}

# Krok 3: Sprawdź czy serwer działa
Write-Host "`n[3/4] Sprawdzanie serwera..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:11434/api/tags" -TimeoutSec 2 -ErrorAction Stop
    Write-Host "✅ Serwer Ollama działa!" -ForegroundColor Green
    $serverRunning = $true
} catch {
    Write-Host "⚠️ Serwer nie działa - uruchom w osobnym terminalu:" -ForegroundColor Yellow
    Write-Host "   ollama serve" -ForegroundColor Cyan
    $serverRunning = $false
}

# Krok 4: Sprawdź modele
Write-Host "`n[4/4] Sprawdzanie zainstalowanych modeli..." -ForegroundColor Yellow
try {
    $models = ollama list
    if ($models -match "llama3.2|mistral|codellama") {
        Write-Host "✅ Modele znalezione:" -ForegroundColor Green
        Write-Host $models
    } else {
        Write-Host "⚠️ Brak modeli - pobierz model:" -ForegroundColor Yellow
        Write-Host "   ollama pull llama3.2" -ForegroundColor Cyan
    }
} catch {
    Write-Host "⚠️ Nie można sprawdzić modeli (serwer może nie działać)" -ForegroundColor Yellow
}

# Podsumowanie
Write-Host "`n" + "=" * 50
Write-Host "✅ Konfiguracja zakończona!" -ForegroundColor Green
Write-Host "`n📝 Następne kroki:" -ForegroundColor Cyan
if (-not $serverRunning) {
    Write-Host "   1. Uruchom serwer: ollama serve" -ForegroundColor White
}
Write-Host "   2. Pobierz model: ollama pull llama3.2" -ForegroundColor White
Write-Host "   3. Użyj w Pythonie: create_demo_assistant(use_local_model=True)" -ForegroundColor White
Write-Host "`n💡 Wskazówka: Zrestartuj terminal aby PATH zadziałał wszędzie" -ForegroundColor Yellow

