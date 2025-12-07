# Test skrypt dla Ollama na Windows
# Uruchom: .\test_ollama.ps1

Write-Host "🔍 Sprawdzanie instalacji Ollama..." -ForegroundColor Cyan

# Sprawdź możliwe lokalizacje
$paths = @(
    "$env:LOCALAPPDATA\Programs\Ollama\ollama.exe",
    "$env:ProgramFiles\Ollama\ollama.exe",
    "$env:ProgramFiles(x86)\Ollama\ollama.exe",
    "C:\ollama\ollama.exe"
)

$found = $false
foreach ($path in $paths) {
    if (Test-Path $path) {
        Write-Host "✅ Znaleziono Ollama: $path" -ForegroundColor Green
        $found = $true
        
        # Sprawdź wersję
        Write-Host "📋 Wersja:" -ForegroundColor Yellow
        & $path --version
        
        # Sprawdź czy serwer działa
        Write-Host "`n🔌 Sprawdzanie serwera Ollama..." -ForegroundColor Cyan
        try {
            $response = Invoke-WebRequest -Uri "http://localhost:11434/api/tags" -TimeoutSec 2 -ErrorAction Stop
            Write-Host "✅ Serwer Ollama działa!" -ForegroundColor Green
        } catch {
            Write-Host "⚠️ Serwer Ollama nie działa" -ForegroundColor Yellow
            Write-Host "   Uruchom: ollama serve" -ForegroundColor Yellow
            Write-Host "   Lub: & '$path' serve" -ForegroundColor Yellow
        }
        break
    }
}

if (-not $found) {
    Write-Host "❌ Ollama nie znaleziono!" -ForegroundColor Red
    Write-Host "`n📥 Instalacja:" -ForegroundColor Cyan
    Write-Host "   1. Pobierz z: https://ollama.ai/download" -ForegroundColor White
    Write-Host "   2. Zainstaluj" -ForegroundColor White
    Write-Host "   3. Zrestartuj terminal" -ForegroundColor White
    Write-Host "`n📖 Więcej informacji: NAPRAWA_OLLAMA_WINDOWS.md" -ForegroundColor Cyan
}

Write-Host "`n✅ Test zakończony" -ForegroundColor Green

