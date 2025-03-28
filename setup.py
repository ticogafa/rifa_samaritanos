#!/usr/bin/env python3
import os
import sys
import platform
import subprocess
import site
import shutil

def clear_screen():
    """Limpa a tela do console em diferentes sistemas operacionais"""
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

def print_header():
    """Exibe o cabeçalho do programa de configuração"""
    print("\n" + "=" * 60)
    print(" CONFIGURAÇÃO DO SISTEMA DE RIFAS ".center(60))
    print(" Samaritanos ".center(60))
    print("=" * 60 + "\n")

def verificar_tkinter():
    """Verifica se o Tkinter está instalado"""
    try:
        import tkinter
        print("✅ Tkinter está instalado corretamente!")
        return True
    except ImportError:
        print("❌ Tkinter não está instalado!")
        return False

def verificar_dependencias():
    """Verifica todas as dependências necessárias"""
    print("Verificando dependências...\n")
    
    tkinter_ok = verificar_tkinter()
    
    # Verificar arquivos essenciais
    arquivos_essenciais = [
        "iniciar_rifa.py", 
        "rifa_manager.py", 
        "rifa_gui.py"
    ]
    
    arquivos_faltando = []
    for arquivo in arquivos_essenciais:
        caminho = os.path.join(os.path.dirname(__file__), arquivo)
        if os.path.exists(caminho):
            print(f"✅ Arquivo {arquivo} encontrado")
        else:
            print(f"⚠️ Arquivo {arquivo} não encontrado!")
            arquivos_faltando.append(arquivo)
    
    # Verificar arquivo de dados
    arquivo_rifas = os.path.join(os.path.dirname(__file__), "rifas.csv")
    if not os.path.exists(arquivo_rifas):
        print("ℹ️ Arquivo rifas.csv não encontrado. Será criado automaticamente ao iniciar o programa.")
    else:
        print("✅ Arquivo rifas.csv encontrado")
    
    print("\nResumo das verificações:")
    if tkinter_ok:
        print("✅ Interface gráfica: Disponível")
    else:
        print("⚠️ Interface gráfica: Não disponível (falta Tkinter)")
    
    if arquivos_faltando:
        print(f"⚠️ Alguns arquivos estão faltando: {', '.join(arquivos_faltando)}")
    else:
        print("✅ Todos os arquivos essenciais estão presentes")
    
    return tkinter_ok

def instalar_tkinter():
    """Fornece instruções para instalação do Tkinter"""
    sistema = platform.system().lower()
    
    print("\nPara instalar o Tkinter (necessário para a interface gráfica):")
    
    if sistema == "linux":
        if os.path.exists("/etc/debian_version"):  # Debian, Ubuntu, etc.
            print("Execute no terminal:")
            print("    sudo apt-get install python3-tk")
        elif os.path.exists("/etc/redhat-release"):  # Fedora, RHEL, etc.
            print("Execute no terminal:")
            print("    sudo dnf install python3-tkinter")
        else:
            print("Execute o comando apropriado para instalar o pacote 'python3-tk' na sua distribuição Linux.")
    
    elif sistema == "darwin":  # macOS
        print("No macOS, você pode instalar o Python com Tkinter através do site oficial:")
        print("    https://www.python.org/downloads/macos/")
        print("Certifique-se de que a opção tcl/tk esteja marcada durante a instalação.")
    
    elif sistema == "windows":
        print("No Windows, reinstale o Python pelo site oficial:")
        print("    https://www.python.org/downloads/windows/")
        print("Durante a instalação, certifique-se de marcar a opção 'tcl/tk and IDLE'.")
    
    print("\nApós a instalação, execute este script novamente.")

def check_python_version():
    """Verifica se a versão do Python é compatível"""
    if sys.version_info < (3, 6):
        print("⚠️ Este programa requer Python 3.6 ou superior.")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro} detectado")
    return True

def install_requirements():
    """Instala as dependências necessárias"""
    print("\n📦 Verificando dependências necessárias...")
    
    # Lista de pacotes necessários (excluímos tkinter pois é tratado separadamente)
    requirements = ["pillow", "pandas", "openpyxl"]
    
    installed_packages = []
    failed_packages = []
    
    for package in requirements:
        try:
            # Verificar se o pacote já está instalado
            __import__(package.lower().replace('-', '_'))
            print(f"✅ {package} já está instalado.")
            installed_packages.append(package)
        except ImportError:
            print(f"ℹ️ Instalando {package}...")
            try:
                # Suprimindo a saída do pip para evitar mensagens de erro desnecessárias
                with open(os.devnull, 'w') as devnull:
                    subprocess.run(
                        [sys.executable, "-m", "pip", "install", "--user", package],
                        check=True,
                        stdout=devnull,
                        stderr=devnull
                    )
                print(f"✅ {package} instalado com sucesso.")
                installed_packages.append(package)
            except subprocess.CalledProcessError:
                print(f"⚠️ Não foi possível instalar {package}. Este pacote não é essencial.")
                failed_packages.append(package)
    
    print(f"\n✅ {len(installed_packages)} pacotes verificados/instalados com sucesso.")
    if failed_packages:
        print(f"⚠️ {len(failed_packages)} pacotes não puderam ser instalados, mas não são essenciais.")
    
    return True

def main():
    clear_screen()
    print_header()
    
    print("Este script irá configurar o Sistema de Rifas Beneficentes.\n")
    
    if not check_python_version():
        print("\n⚠️ Versão do Python incompatível.")
        print("   Por favor, instale o Python 3.6 ou superior e execute este script novamente.")
        input("\nPressione ENTER para sair...")
        return False
    
    # Verificar dependências
    tkinter_ok = verificar_dependencias()
    
    # Se faltar o Tkinter, fornecer instruções de instalação
    if not tkinter_ok:
        print("\nℹ️ O Tkinter é necessário para a interface gráfica.")
        instalar_tkinter()
    
    # Instalar dependências Python
    deps_ok = install_requirements()
    
    print("\n" + "=" * 60)
    print("✅ Configuração concluída!")
    print("\nPara iniciar o programa:")
    print("Execute o arquivo 'iniciar_rifa.py' ou 'python iniciar_rifa.py'")
    
    if not tkinter_ok:
        print("\nℹ️ Nota: A interface gráfica não estará disponível até que o Tkinter seja instalado.")
        print("   O programa irá funcionar apenas no modo de terminal.")
    
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nℹ️ Configuração cancelada pelo usuário.")
    except Exception as e:
        print(f"\n⚠️ Ocorreu um erro inesperado: {e}")
        print("   Por favor, tente executar o script novamente.")
        input("\nPressione ENTER para sair...")
