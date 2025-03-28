@echo off
title Sistema de Rifas Samaritanos
cls
echo Iniciando Sistema de Rifas...
python iniciar_rifa.py
if errorlevel 1 (
    echo.
    echo Ocorreu um erro ao iniciar o programa.
    echo Verifique se o Python esta instalado corretamente.
    pause
)
