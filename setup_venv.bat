@echo off
REM Skrypt do tworzenia wirtualnego środowiska dla projektu HackNation

echo ========================================
echo Tworzenie wirtualnego środowiska
echo ========================================

REM Sprawdź czy Python jest dostępny
python --version >nul 2>&1
if errorlevel 1 (
    echo BŁĄD: Python nie jest zainstalowany lub nie jest w PATH
    pause
    exit /b 1
)

REM Utwórz wirtualne środowisko
echo [1/3] Tworzenie wirtualnego środowiska...
python -m venv venv

if errorlevel 1 (
    echo BŁĄD: Nie można utworzyć wirtualnego środowiska
    pause
    exit /b 1
)

REM Aktywuj środowisko
echo [2/3] Aktywacja środowiska...
call venv\Scripts\activate.bat

REM Zaktualizuj pip
echo [3/3] Aktualizacja pip...
python -m pip install --upgrade pip

REM Zainstaluj wymagania dla asystenta (Foreground IP)
echo.
echo ========================================
echo Instalacja wymagań dla Asystenta AI
echo ========================================
cd AIWSLUZBIE
pip install -r requirements.txt
cd ..

REM Opcjonalnie: Zainstaluj wymagania dla GQPA (Background IP)
echo.
echo ========================================
echo Instalacja wymagań dla GQPA Core (opcjonalne)
echo ========================================
echo Czy chcesz zainstalować wymagania dla GQPA Core? (t/n)
set /p install_gqpa=
if /i "%install_gqpa%"=="t" (
    cd gqpa_core
    pip install -r requirements.txt
    cd ..
)

echo.
echo ========================================
echo ✅ ŚRODOWISKO GOTOWE!
echo ========================================
echo.
echo Aby aktywować środowisko w przyszłości:
echo   venv\Scripts\activate.bat
echo.
echo Aby dezaktywować:
echo   deactivate
echo.
pause

