@echo off
echo ========================================
echo Instalacja zaleznosci dla Scenariusze Jutra
echo ========================================
echo.

cd /d "%~dp0"

echo Instalowanie zaleznosci z requirements.txt...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

echo.
echo ========================================
echo Instalacja zakonczona!
echo ========================================
pause

