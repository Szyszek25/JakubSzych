@echo off
echo ============================================================
echo   URUCHAMIANIE BACKEND API DASHBOARD
echo ============================================================
echo.

cd /d %~dp0

echo Sprawdzanie zaleznosci...
python -c "import fastapi" 2>nul
if errorlevel 1 (
    echo Instalowanie FastAPI...
    pip install fastapi uvicorn pydantic
    echo.
)

echo Uruchamianie API Dashboard...
echo API bedzie dostepne na: http://localhost:8000
echo Dokumentacja: http://localhost:8000/docs
echo.
echo Nacisnij Ctrl+C aby zatrzymac
echo.

python api_dashboard.py

