import csv
import os
import sys
from datetime import datetime

class RifaManager:
    def __init__(self, arquivo_csv='rifas.csv'):
        self.arquivo_csv = arquivo_csv
        self.headers = ['numero', 'nome', 'telefone', 'data_compra']
        self.verificar_arquivo()
    
    def verificar_arquivo(self):
        """Verifica se o arquivo CSV existe, se não, cria com cabeçalhos."""
        if not os.path.exists(self.arquivo_csv):
            with open(self.arquivo_csv, 'w', newline='', encoding='utf-8') as arquivo:
                writer = csv.writer(arquivo)
                writer.writerow(self.headers)
    
    def cadastrar_comprador(self, numero, nome, telefone):
        """Cadastra um novo comprador de rifa."""
        # Verificar se o número já está cadastrado
        if self.buscar_por_numero(numero):
            return False, f"Erro: Número {numero} já está cadastrado."
        
        data_compra = datetime.now().strftime("%d/%m/%Y %H:%M")
        
        with open(self.arquivo_csv, 'a', newline='', encoding='utf-8') as arquivo:
            writer = csv.writer(arquivo)
            writer.writerow([numero, nome, telefone, data_compra])
        
        return True, f"Comprador {nome} cadastrado com o número {numero}."
    
    def cadastrar_multiplos_numeros(self, numeros, nome, telefone):
        """Cadastra múltiplos números de rifa para o mesmo comprador."""
        data_compra = datetime.now().strftime("%d/%m/%Y %H:%M")
        numeros_cadastrados = []
        numeros_com_erro = []
        
        for numero in numeros:
            # Verificar se o número já está cadastrado
            if self.buscar_por_numero(numero):
                numeros_com_erro.append(numero)
                continue
            
            with open(self.arquivo_csv, 'a', newline='', encoding='utf-8') as arquivo:
                writer = csv.writer(arquivo)
                writer.writerow([numero, nome, telefone, data_compra])
                numeros_cadastrados.append(numero)
        
        mensagem = ""
        if numeros_cadastrados:
            mensagem += f"Comprador {nome} cadastrado com os números: {', '.join(numeros_cadastrados)}.\n"
        if numeros_com_erro:
            mensagem += f"Números já cadastrados: {', '.join(numeros_com_erro)}."
        
        return bool(numeros_cadastrados), mensagem.strip()
    
    def listar_compradores(self):
        """Lista todos os compradores cadastrados ordenados pelo número da rifa."""
        compradores = []
        
        with open(self.arquivo_csv, 'r', encoding='utf-8') as arquivo:
            reader = csv.DictReader(arquivo)
            for row in reader:
                compradores.append(row)
        
        # Ordenar pelo número da rifa (convertendo para int para ordenação numérica)
        compradores.sort(key=lambda x: int(x['numero']))
        
        return compradores
    
    def buscar_por_numero(self, numero):
        """Busca um comprador pelo número da rifa."""
        with open(self.arquivo_csv, 'r', encoding='utf-8') as arquivo:
            reader = csv.DictReader(arquivo)
            for row in reader:
                if row['numero'] == str(numero):
                    return row
        return None
    
    def buscar_por_nome(self, nome):
        """Busca compradores pelo nome (busca parcial)."""
        resultados = []
        nome = nome.lower()
        
        with open(self.arquivo_csv, 'r', encoding='utf-8') as arquivo:
            reader = csv.DictReader(arquivo)
            for row in reader:
                if nome in row['nome'].lower():
                    resultados.append(row)
        
        return resultados
    
    def exportar_para_csv(self, arquivo_destino):
        """Exporta os dados para um novo arquivo CSV."""
        import shutil
        shutil.copy(self.arquivo_csv, arquivo_destino)
        return True, f"Dados exportados para {arquivo_destino}"

def mostrar_menu():
    print("\n=== SISTEMA DE GERENCIAMENTO DE RIFAS ===")
    print("1. Cadastrar novo comprador")
    print("2. Cadastrar múltiplos números para um comprador")
    print("3. Listar todos os compradores")
    print("4. Buscar por número da rifa")
    print("5. Buscar por nome")
    print("6. Exportar dados")
    print("0. Sair")
    return input("Escolha uma opção: ")

def main():
    rifa = RifaManager()
    
    while True:
        opcao = mostrar_menu()
        
        if opcao == '1':
            numero = input("Número da rifa: ")
            nome = input("Nome do comprador: ")
            telefone = input("Telefone: ")
            
            sucesso, mensagem = rifa.cadastrar_comprador(numero, nome, telefone)
            print(mensagem)
            
        elif opcao == '2':
            numeros_input = input("Números da rifa (separados por vírgula): ")
            numeros = [num.strip() for num in numeros_input.split(',')]
            nome = input("Nome do comprador: ")
            telefone = input("Telefone: ")
            
            sucesso, mensagem = rifa.cadastrar_multiplos_numeros(numeros, nome, telefone)
            print(mensagem)
            
        elif opcao == '3':
            compradores = rifa.listar_compradores()
            if not compradores:
                print("Nenhum comprador cadastrado ainda.")
            else:
                print("\n=== COMPRADORES CADASTRADOS ===")
                print(f"{'Número':<10} {'Nome':<30} {'Telefone':<15} {'Data da Compra':<20}")
                print('-' * 75)
                for c in compradores:
                    print(f"{c['numero']:<10} {c['nome']:<30} {c['telefone']:<15} {c['data_compra']:<20}")
            
        elif opcao == '4':
            numero = input("Digite o número da rifa: ")
            comprador = rifa.buscar_por_numero(numero)
            
            if comprador:
                print("\n=== RESULTADO DA BUSCA ===")
                print(f"Número: {comprador['numero']}")
                print(f"Nome: {comprador['nome']}")
                print(f"Telefone: {comprador['telefone']}")
                print(f"Data da Compra: {comprador['data_compra']}")
            else:
                print(f"Nenhum comprador encontrado com o número {numero}.")
            
        elif opcao == '5':
            nome = input("Digite o nome (ou parte dele) para buscar: ")
            resultados = rifa.buscar_por_nome(nome)
            
            if resultados:
                print("\n=== RESULTADOS DA BUSCA ===")
                print(f"{'Número':<10} {'Nome':<30} {'Telefone':<15} {'Data da Compra':<20}")
                print('-' * 75)
                for r in resultados:
                    print(f"{r['numero']:<10} {r['nome']:<30} {r['telefone']:<15} {r['data_compra']:<20}")
            else:
                print(f"Nenhum comprador encontrado com o nome '{nome}'.")
            
        elif opcao == '6':
            nome_arquivo = input("Digite o nome do arquivo para exportação (ex: rifas_backup.csv): ")
            sucesso, mensagem = rifa.exportar_para_csv(nome_arquivo)
            print(mensagem)
            
        elif opcao == '0':
            print("Saindo do sistema...")
            break
            
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
