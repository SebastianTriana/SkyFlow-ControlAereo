@echo off
title SkyFlow - Torre de Control (Consola)
cd /d "%~dp0"
python main.py
if errorlevel 1 (
    echo.
    echo Ocurrio un error al ejecutar la consola.
    pause
)
