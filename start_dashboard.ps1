# 🚀 Skrypt uruchomienia Dashboard (Backend + Frontend)
# Uruchamia backend API i frontend dashboard

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  🏛️ ASYSTENT AI DASHBOARD - URUCHOMIENIE" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Sprawdź czy backend działa
$backendRunning = $false
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000" -TimeoutSec 2 -ErrorAction Stop
    $backendRunning = $true
    Write-Host "✅ Backend API już działa na porcie 8000" -ForegroundColor Green
} catch {
    Write-Host "⚠️ Backend API nie działa - uruchom w osobnym terminalu:" -ForegroundColor Yellow
    Write-Host "   cd AIWSLUZBIE" -ForegroundColor Yellow
    Write-Host "   python api_dashboard.py" -ForegroundColor Yellow
    Write-Host ""
}

# Uruchom frontend
Write-Host "🚀 Uruchamianie frontend dashboard..." -ForegroundColor Cyan
Write-Host ""

Set-Location dashboard-frontend

if (-not (Test-Path node_modules)) {
    Write-Host "📦 Instalowanie zależności..." -ForegroundColor Yellow
    npm install
    Write-Host ""
}

Write-Host "✅ Frontend będzie dostępny na: http://localhost:3000" -ForegroundColor Green
Write-Host "📚 Backend API: http://localhost:8000" -ForegroundColor Green
Write-Host "📖 API Docs: http://localhost:8000/docs" -ForegroundColor Green
Write-Host ""
Write-Host "Naciśnij Ctrl+C aby zatrzymać" -ForegroundColor Yellow
Write-Host ""

npm run dev

