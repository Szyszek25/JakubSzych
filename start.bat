@echo off
chcp 65001 >nul
REM Wrapper dla Windows - uruchamia start_scenariusze_jutra.py
python start_scenariusze_jutra.py
if errorlevel 1 (
    echo.
    echo BLAD podczas uruchamiania!
    pause
)

