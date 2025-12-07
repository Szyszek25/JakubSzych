# Dodaj Ollama do PATH na stale (dla uzytkownika)
# Uruchom: .\dodaj_ollama_na_stale.ps1

Write-Host "Dodawanie Ollama do PATH na stale..." -ForegroundColor Cyan

$ollamaPath = "$env:LOCALAPPDATA\Programs\Ollama"

if (Test-Path "$ollamaPath\ollama.exe") {
    # Pobierz aktualny PATH uzytkownika
    $currentPath = [Environment]::GetEnvironmentVariable("Path", "User")
    
    if ($currentPath -notlike "*$ollamaPath*") {
        # Dodaj Ollama do PATH
        $newPath = $currentPath + ";$ollamaPath"
        [Environment]::SetEnvironmentVariable("Path", $newPath, "User")
        
        Write-Host "Ollama dodane do PATH na stale!" -ForegroundColor Green
        Write-Host ""
        Write-Host "Sciezka dodana: $ollamaPath" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "WAZNE: Zrestartuj terminal aby zmiany zadzialaly!" -ForegroundColor Cyan
        Write-Host "   (Zamknij i otworz nowy PowerShell)" -ForegroundColor Gray
    } else {
        Write-Host "Ollama juz jest w PATH!" -ForegroundColor Green
    }
    
    # Dodaj tez do biezacej sesji
    $env:Path += ";$ollamaPath"
    Write-Host ""
    Write-Host "Ollama dodane do PATH tej sesji" -ForegroundColor Green
    
    # Test
    Write-Host ""
    Write-Host "Test:" -ForegroundColor Cyan
    ollama --version
    
} else {
    Write-Host "Ollama nie znaleziono w: $ollamaPath" -ForegroundColor Red
    Write-Host "   Zainstaluj z: https://ollama.ai/download" -ForegroundColor Yellow
}
