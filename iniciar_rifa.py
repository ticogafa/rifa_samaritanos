#!/usr/bin/env python3
import os
import sys
import platform
import subprocess

def clear_screen():
    """Limpa a tela do console em diferentes sistemas operacionais"""
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

def print_header():
    """Exibe o cabeçalho do programa"""
    print("\n" + "=" * 60)
    print(" SISTEMA DE RIFAS BENEFICENTES ".center(60))
    print(" Samaritanos ".center(60))
    print("=" * 60 + "\n")

def verificar_dependencias():
    """Verifica se o Tkinter está instalado"""
    try:
        import tkinter
        return True
    except ImportError:
        return False

def iniciar_programa():
    """Inicia o programa diretamente com a interface gráfica"""
    clear_screen()
    print_header()
    
    # Verifica se tkinter está instalado
    tkinter_ok = verificar_dependencias()
    
    if tkinter_ok:
        print("Iniciando a interface gráfica...\n")
        subprocess.call([sys.executable, "rifa_gui.py"])
    else:
        print("\n⚠️ A interface gráfica requer Tkinter, que não está instalado.")
        print("\nPara instalar Tkinter:")
        
        system = platform.system().lower()
        if system == "linux":
            if os.path.exists('/etc/debian_version'):
                print("   Execute: sudo apt-get install python3-tk")
            elif os.path.exists('/etc/redhat-release'):
                print("   Execute: sudo dnf install python3-tkinter")
            else:
                print("   Instale o pacote 'python3-tk' para sua distribuição")
        elif system == "darwin":  # macOS
            print("   No macOS, reinstale o Python através do site oficial com Tkinter.")
        elif system == "windows":
            print("   No Windows, reinstale o Python marcando a opção 'tcl/tk'.")
        
        print("\nApós instalar o Tkinter, execute este programa novamente.")
    

if __name__ == "__main__":
    try:
        iniciar_programa()
    except Exception as e:
        print(f"\n⚠️ Ocorreu um erro: {e}")
        input("\nPressione ENTER para sair...")
