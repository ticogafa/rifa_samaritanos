# Sistema de Gerenciamento de Rifas Beneficentes

Este é um sistema completo para gerenciar rifas beneficentes, desenvolvido para os Samaritanos. Funciona em Windows, macOS e Linux.

## 📋 Funcionalidades

O sistema oferece as seguintes funcionalidades principais:

- **Cadastro de rifas**: Registre compradores com seus números, nomes e telefones
- **Cadastro múltiplo**: Adicione vários números para um mesmo comprador
- **Busca avançada**: Encontre rifas por número ou por nome do comprador
- **Exportação de dados**: Exporte os dados para arquivo CSV
- **Importação de dados**: Importe registros de arquivos CSV externos
- **Interface gráfica amigável**: Fácil de usar para qualquer pessoa

## 🚀 Como Iniciar

### Primeira Instalação

1. **Configure o ambiente**:
   - Execute o arquivo `setup.py` para verificar dependências:
     - No Windows: Dê duplo clique em `setup.py`
     - No Mac/Linux: Execute `python3 setup.py`

2. **Inicie o programa**:
   - Execute `python iniciar_rifa.py` ou `python3 iniciar_rifa.py`

## 🖥️ Estrutura do Projeto

O sistema está organizado nos seguintes componentes:

| Arquivo | Descrição |
|---------|-----------|
| `iniciar_rifa.py` | Ponto de entrada principal do programa |
| `rifa_manager.py` | Núcleo do sistema - gerencia dados e operações |
| `rifa_gui.py` | Interface gráfica do usuário (GUI) |
| `csv_merger.py` | Ferramenta para importar dados de outros arquivos CSV |
| `setup.py` | Configuração inicial e verificação de dependências |
| `rifas.csv` | Banco de dados local em formato CSV |

## 📊 Gerenciamento de Dados

- **Armazenamento**: Os dados são armazenados no arquivo `rifas.csv`
- **Campos**: Cada registro contém número da rifa, nome, telefone e data da compra
- **Segurança**: Faça backups regulares usando a função de exportação
- **Importação**: Combine dados de diferentes fontes com a função de importação CSV

## 📱 Interface Gráfica

A interface gráfica inclui as seguintes abas:

1. **Cadastro**: Registre novos compradores e seus números
2. **Listar Compradores**: Visualize todos os compradores cadastrados
3. **Buscar**: Encontre compradores por número ou nome
4. **Exportar**: Salve os dados para um arquivo CSV externo
5. **Importar CSV**: Importe dados de arquivos CSV externos

## 🔧 Requisitos Técnicos

- **Python**: Versão 3.6 ou superior
- **Bibliotecas principais**:
  - Tkinter: Para a interface gráfica
  - Pandas/CSV: Para manipulação de dados
  - Pillow: Para elementos gráficos adicionais

## 💡 Dicas de Uso

- **Cadastro múltiplo**: Use vírgulas para separar números ao cadastrar várias rifas para um mesmo comprador
- **Busca parcial**: Ao buscar por nome, pode-se inserir apenas parte do nome
- **Exportação regular**: Exporte os dados regularmente como backup
- **Importação**: Útil para combinar vendas registradas em diferentes computadores

## ❓ Resolução de Problemas

Se encontrar dificuldades:

1. **Sem interface gráfica?** Verifique se o Tkinter está instalado:
   - Windows/macOS: Normalmente vem com a instalação do Python
   - Linux: Execute `sudo apt-get install python3-tk` (Debian/Ubuntu) ou equivalente

2. **Erros na importação?** Verifique se o arquivo CSV tem os cabeçalhos corretos:
   - Deve conter pelo menos as colunas: `numero`, `nome` e `telefone`

3. **Instalação**: Execute novamente o `setup.py` para verificar todas as dependências

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo LICENSE para detalhes.
