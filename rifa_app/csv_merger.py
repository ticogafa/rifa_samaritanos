import csv
import os
import sys
from datetime import datetime 

def merge_csv_files(arquivo_destino='rifas.csv', arquivo_origem=None):
    """
    Mescla um arquivo CSV externo com o arquivo de rifas local.
    Trata números repetidos, mantendo apenas a primeira ocorrência.
    
    Args:
        arquivo_destino: Arquivo CSV destino (padrão: rifas.csv)
        arquivo_origem: Arquivo CSV de origem a ser mesclado
        
    Returns:
        tuple: (sucesso, mensagem, estatísticas)
    """
    if not arquivo_origem or not os.path.exists(arquivo_origem):
        return False, "Arquivo de origem não encontrado.", {}
        
    # Verificar se o arquivo de destino existe
    if not os.path.exists(arquivo_destino):
        with open(arquivo_destino, 'w', newline='', encoding='utf-8') as arquivo:
            writer = csv.writer(arquivo)
            writer.writerow(['numero', 'nome', 'telefone', 'data_compra'])
    
    # Ler números existentes no arquivo de destino
    numeros_existentes = set()
    dados_destino = []
    
    with open(arquivo_destino, 'r', encoding='utf-8') as arquivo:
        reader = csv.DictReader(arquivo)
        for row in reader:
            numeros_existentes.add(row['numero'])
            dados_destino.append(row)
    
    # Ler dados do arquivo de origem
    dados_origem = []
    cabecalhos_validos = False
    numeros_adicionados = []
    numeros_ignorados = []
    
    try:
        with open(arquivo_origem, 'r', encoding='utf-8') as arquivo:
            reader = csv.reader(arquivo)
            headers = next(reader, None)
            
            # Verificar se os cabeçalhos existem e contêm pelo menos 'numero' e 'nome'
            cabecalhos_validos = headers and 'numero' in headers and 'nome' in headers
            
            if not cabecalhos_validos:
                return False, "Formato de arquivo inválido. Cabeçalhos necessários: numero, nome", {}
            
            # Mapear índices dos cabeçalhos
            idx_numero = headers.index('numero')
            idx_nome = headers.index('nome')
            idx_telefone = headers.index('telefone') if 'telefone' in headers else -1
            idx_data = headers.index('data_compra') if 'data_compra' in headers else -1
            
            # Processar dados
            for row in reader:
                if len(row) > idx_numero and len(row) > idx_nome:
                    numero = row[idx_numero].strip()
                    nome = row[idx_nome].strip()
                    telefone = row[idx_telefone] if idx_telefone >= 0 and idx_telefone < len(row) else ""
                    
                    # Verificar se o número já existe
                    if numero in numeros_existentes:
                        numeros_ignorados.append(numero)
                        continue
                    
                    # Adicionar nova entrada
                    data_compra = datetime.now().strftime("%d/%m/%Y %H:%M")
                    numeros_existentes.add(numero)
                    numeros_adicionados.append(numero)
                    
                    dados_origem.append({
                        'numero': numero,
                        'nome': nome,
                        'telefone': telefone,
                        'data_compra': data_compra
                    })
    except Exception as e:
        return False, f"Erro ao ler o arquivo: {str(e)}", {}
    
    # Escrever dados mesclados de volta ao arquivo de destino
    with open(arquivo_destino, 'w', newline='', encoding='utf-8') as arquivo:
        writer = csv.DictWriter(arquivo, fieldnames=['numero', 'nome', 'telefone', 'data_compra'])
        writer.writeheader()
        
        # Escrever dados originais
        for row in dados_destino:
            writer.writerow(row)
        
        # Escrever novos dados
        for row in dados_origem:
            writer.writerow(row)
    
    # Preparar estatísticas
    estatisticas = {
        'total_adicionados': len(numeros_adicionados),
        'total_ignorados': len(numeros_ignorados),
        'numeros_adicionados': numeros_adicionados,
        'numeros_ignorados': numeros_ignorados
    }
    
    mensagem = f"Importação concluída. {len(numeros_adicionados)} números adicionados."
    if numeros_ignorados:
        mensagem += f" {len(numeros_ignorados)} números ignorados por já existirem."
    
    return True, mensagem, estatisticas

if __name__ == "__main__":
    if len(sys.argv) > 1:
        arquivo_origem = sys.argv[1]
        sucesso, mensagem, stats = merge_csv_files(arquivo_origem=arquivo_origem)
        print(mensagem)
        
        if sucesso and stats['total_adicionados'] > 0:
            print("\nNúmeros adicionados:")
            for num in stats['numeros_adicionados']:
                print(f" - {num}")
        
        if stats['total_ignorados'] > 0:
            print("\nNúmeros ignorados (já existentes):")
            for num in stats['numeros_ignorados']:
                print(f" - {num}")
    else:
        print("Uso: python csv_merger.py arquivo_origem.csv")
