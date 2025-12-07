# Dodaj Ollama do PATH w bieżącej sesji PowerShell
# Uruchom: .\dodaj_ollama_do_path.ps1

$ollamaPath = "$env:LOCALAPPDATA\Programs\Ollama"

if (Test-Path "$ollamaPath\ollama.exe") {
    # Dodaj do PATH dla tej sesji
    $env:Path += ";$ollamaPath"
    
    Write-Host "✅ Ollama dodane do PATH" -ForegroundColor Green
    Write-Host "`n📋 Test:" -ForegroundColor Cyan
    ollama --version
    
    Write-Host "`n📦 Zainstalowane modele:" -ForegroundColor Cyan
    ollama list
    
    Write-Host "`n🚀 Aby uruchomić serwer:" -ForegroundColor Yellow
    Write-Host "   ollama serve" -ForegroundColor White
    
    Write-Host "`n💡 Wskazówka: Aby dodać na stałe, zrestartuj terminal po instalacji Ollama" -ForegroundColor Gray
} else {
    Write-Host "❌ Ollama nie znaleziono w: $ollamaPath" -ForegroundColor Red
    Write-Host "   Zainstaluj z: https://ollama.ai/download" -ForegroundColor Yellow
}

