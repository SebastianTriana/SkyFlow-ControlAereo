@echo off
title SkyFlow - Interfaz Grafica
cd /d "%~dp0"
python gui.py
if errorlevel 1 (
    echo.
    echo Ocurrio un error al ejecutar la interfaz grafica.
    pause
)
