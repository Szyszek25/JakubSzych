@echo off
REM Skrypt do tworzenia wirtualnego środowiska dla GQPA Core (Background IP)

echo ========================================
echo Tworzenie wirtualnego środowiska GQPA
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
python -m venv venv_gqpa

if errorlevel 1 (
    echo BŁĄD: Nie można utworzyć wirtualnego środowiska
    pause
    exit /b 1
)

REM Aktywuj środowisko
echo [2/3] Aktywacja środowiska...
call venv_gqpa\Scripts\activate.bat

REM Zaktualizuj pip
echo [3/3] Aktualizacja pip...
python -m pip install --upgrade pip

REM Zainstaluj wymagania dla GQPA
echo.
echo ========================================
echo Instalacja wymagań dla GQPA Core
echo ========================================
cd gqpa_core
pip install -r requirements.txt
cd ..

echo.
echo ========================================
echo ✅ ŚRODOWISKO GQPA GOTOWE!
echo ========================================
echo.
echo Aby aktywować środowisko w przyszłości:
echo   venv_gqpa\Scripts\activate.bat
echo.
echo Aby dezaktywować:
echo   deactivate
echo.
pause

