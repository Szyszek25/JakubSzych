@echo off
echo ========================================
echo ZANT - ZUS Accident Notification Tool
echo ========================================
echo.

echo [1/3] Sprawdzam Google Gemini API Key...
if "%GOOGLE_API_KEY%"=="" (
    if exist .env (
        echo ✅ Znaleziono plik .env
    ) else (
        echo ⚠️ GOOGLE_API_KEY nie ustawione!
        echo.
        echo Ustaw zmienną środowiskową:
        echo   set GOOGLE_API_KEY=twój_klucz
        echo.
        echo LUB utwórz plik .env z:
        echo   GOOGLE_API_KEY=twój_klucz
        echo.
        echo Uzyskaj klucz na: https://aistudio.google.com/
        echo.
        pause
        exit /b 1
    )
) else (
    echo ✅ GOOGLE_API_KEY ustawione
)
echo.

echo [2/3] Instaluje zależności...
pip install -r requirements.txt
echo.

echo [3/3] Uruchamiam backend...
echo.
echo 🌐 Backend będzie dostępny na: http://localhost:8000
echo 📄 Frontend: otwórz frontend/index.html w przeglądarce
echo.
echo Naciśnij Ctrl+C aby zatrzymać
echo.

cd backend
python -m api.main

