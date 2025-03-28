#!/bin/bash
clear
echo "Iniciando Sistema de Rifas..."
python3 iniciar_rifa.py
if [ $? -ne 0 ]; then
    echo ""
    echo "Ocorreu um erro ao iniciar o programa."
    echo "Verifique se o Python está instalado corretamente."
    read -p "Pressione ENTER para continuar..."
fi
