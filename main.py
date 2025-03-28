import os
import sys
import platform

def limpar_tela():
    """Limpa a tela do terminal em diferentes sistemas operacionais"""
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

def verificar_tkinter():
    """Verifica se o Tkinter está disponível"""
    try:
        import tkinter
        return True
    except ImportError:
        return False

def main():
    limpar_tela()
    print("\n" + "=" * 50)
    print(" SISTEMA DE RIFAS SAMARITANOS ".center(50))
    print("=" * 50)
    
    # Verifica se o Tkinter está disponível
    if not verificar_tkinter():
        print("\n⚠️ A interface gráfica requer a biblioteca Tkinter, que não está instalada.")
        print("   Execute o script setup.py para configurar o programa.")
        input("\nPressione ENTER para sair...")
        return
    
    # Inicia diretamente a interface gráfica
    try:
        print("\nIniciando interface gráfica...\n")
        from rifa_gui import main as gui_main
        gui_main()
    except Exception as e:
        print(f"\n⚠️ Erro ao iniciar a interface gráfica: {e}")
        input("\nPressione ENTER para sair...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nPrograma encerrado pelo usuário.")
        sys.exit(0)
    except Exception as e:
        print(f"\n⚠️ Ocorreu um erro não esperado: {e}")
        print("Por favor, execute o script de configuração (setup.py) para resolver problemas.")
        input("\nPressione ENTER para sair...")
        sys.exit(1)
