@echo off
echo ============================================================
echo   URUCHAMIANIE DASHBOARD FRONTEND
echo ============================================================
echo.

if not exist node_modules (
    echo Instalowanie zaleznosci...
    call npm install
    echo.
)

echo Uruchamianie serwera deweloperskiego...
echo Dashboard bedzie dostepny na: http://localhost:3000
echo.
call npm run dev

