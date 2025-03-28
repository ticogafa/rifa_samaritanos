# Sistema de Gerenciamento de Rifas Beneficentes

Este é um sistema simples para gerenciar rifas beneficentes, criado para os Samaritanos. Funciona em Windows, macOS e Linux.

## 📋 Como Usar (Para Usuários)

### Primeira vez usando o programa:

1. **Baixe o programa**:
   - Clique no botão verde "Code" no GitHub e escolha "Download ZIP"
   - Extraia a pasta para qualquer local do seu computador

2. **Execute o instalador**:
   - No Windows: Dê duplo clique em `setup.py`
   - No Mac/Linux: Abra o terminal na pasta e digite `python3 setup.py`

3. **Inicie o programa**:
   - No Windows: Dê duplo clique em `iniciar_rifa.bat` (ou `iniciar_rifa.py`)
   - No Mac/Linux: Dê duplo clique em `iniciar_rifa.py` ou execute `./iniciar_rifa.sh`

### Usando o programa no dia a dia:

1. Execute o arquivo de inicialização (`iniciar_rifa.bat`, `iniciar_rifa.sh` ou `iniciar_rifa.py`)
2. Escolha a interface que deseja usar:
   - **Interface de texto**: funciona em qualquer computador
   - **Interface gráfica**: mais fácil de usar, requer Tkinter instalado
   - **Sincronização com Google Sheets**: para compartilhar os dados online

### Funcionalidades principais:

- **Cadastrar nova rifa**: adicione nome, telefone e número da rifa do comprador
- **Listar todas as rifas**: veja todas as rifas vendidas
- **Buscar**: encontre rifas por número ou nome
- **Exportar dados**: salve os dados em um arquivo CSV de backup

## 🔧 Requisitos Técnicos

- Python 3.6 ou superior
- Para interface gráfica: Tkinter (incluído na maioria das instalações Python)
- Para sincronização com Google Sheets:
  - Bibliotecas `gspread` e `oauth2client`
  - Arquivo de credenciais do Google Cloud Platform (`credentials.json`)

## 🔄 Sincronização com Google Sheets (Opcional)

Para usar a funcionalidade de sincronização com o Google Sheets:

1. Crie um projeto no [Google Cloud Console](https://console.cloud.google.com/)
2. Ative as APIs do Google Sheets e Google Drive
3. Crie uma conta de serviço e baixe as credenciais como `credentials.json`
4. Coloque o arquivo `credentials.json` na pasta do programa

## 📁 Dados e Backup

- O programa salva os dados no arquivo `rifas.csv` na mesma pasta
- Este arquivo pode ser aberto no Excel ou qualquer editor de planilhas
- Faça backups regularmente usando a função "Exportar" no programa

## ❓ Resolução de Problemas

Se você encontrar problemas:

1. Verifique se tem Python instalado
   - Abra o terminal (ou prompt de comando) e digite: `python --version` ou `python3 --version`
   - Se não estiver instalado, baixe em [python.org](https://www.python.org/downloads/)

2. Execute o script de configuração novamente
   - Execute `setup.py` para verificar e instalar componentes necessários

3. Ainda com problemas?
   - Consulte a documentação ou entre em contato com o suporte

## 🛠️ Para Desenvolvedores

- O código-fonte está organizado nos seguintes arquivos:
  - `rifa_manager.py`: Núcleo do sistema (interface de texto)
  - `rifa_gui.py`: Interface gráfica
  - `google_sheets_sync.py`: Integração com Google Sheets
  - `main.py`: Ponto de entrada antigo do programa
  - `iniciar_rifa.py`: Novo ponto de entrada amigável
  - `setup.py`: Configuração e instalação de dependências

- Modifique o código conforme necessário, mantendo a compatibilidade com a estrutura existente
