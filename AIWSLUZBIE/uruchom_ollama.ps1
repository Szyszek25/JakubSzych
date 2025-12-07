# Skrypt do uruchomienia Ollama na Windows
# Uruchom: .\uruchom_ollama.ps1

Write-Host "🚀 Uruchamianie Ollama..." -ForegroundColor Cyan

# Znajdź Ollama
$ollamaPath = "$env:LOCALAPPDATA\Programs\Ollama\ollama.exe"

if (Test-Path $ollamaPath) {
    Write-Host "✅ Znaleziono Ollama: $ollamaPath" -ForegroundColor Green
    
    # Dodaj do PATH dla tej sesji
    $env:Path += ";$env:LOCALAPPDATA\Programs\Ollama"
    
    Write-Host "`n📋 Sprawdzanie wersji..." -ForegroundColor Yellow
    & $ollamaPath --version
    
    Write-Host "`n🔌 Uruchamianie serwera Ollama..." -ForegroundColor Yellow
    Write-Host "   (Naciśnij Ctrl+C aby zatrzymać)" -ForegroundColor Gray
    Write-Host ""
    
    # Uruchom serwer
    & $ollamaPath serve
} else {
    Write-Host "❌ Ollama nie znaleziono w: $ollamaPath" -ForegroundColor Red
    Write-Host "`n📥 Zainstaluj Ollama:" -ForegroundColor Cyan
    Write-Host "   1. Pobierz z: https://ollama.ai/download" -ForegroundColor White
    Write-Host "   2. Zainstaluj" -ForegroundColor White
    Write-Host "   3. Uruchom ten skrypt ponownie" -ForegroundColor White
}

