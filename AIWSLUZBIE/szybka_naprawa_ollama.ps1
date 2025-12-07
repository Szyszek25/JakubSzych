# Szybka naprawa Ollama - dodaj do PATH
# Uruchom: .\szybka_naprawa_ollama.ps1

$ollamaPath = "$env:LOCALAPPDATA\Programs\Ollama"

# Dodaj do PATH biezacej sesji
$env:Path += ";$ollamaPath"

# Dodaj do PATH na stale
$userPath = [Environment]::GetEnvironmentVariable("Path", "User")
if ($userPath -notlike "*$ollamaPath*") {
    [Environment]::SetEnvironmentVariable("Path", "$userPath;$ollamaPath", "User")
    Write-Host "Ollama dodane do PATH na stale!" -ForegroundColor Green
} else {
    Write-Host "Ollama juz jest w PATH" -ForegroundColor Green
}

# Test
Write-Host "Test:" -ForegroundColor Cyan
ollama --version

Write-Host ""
Write-Host "Gotowe! Zrestartuj terminal aby PATH zadzialal wszędzie." -ForegroundColor Yellow

