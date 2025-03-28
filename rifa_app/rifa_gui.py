import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
from rifa_manager import RifaManager
from csv_merger import merge_csv_files

# Cores do tema
CORES = {
    "primaria": "#1976D2",       # Azul escuro
    "secundaria": "#2196F3",     # Azul claro
    "destaque": "#FFC107",       # Amarelo
    "texto": "#212121",          # Quase preto
    "background": "#F5F5F5",     # Cinza claro
    "sucesso": "#4CAF50",        # Verde
    "erro": "#F44336",           # Vermelho
    "aviso": "#FF9800",          # Laranja
    "branco": "#FFFFFF"          # Branco
}

class RifaGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gerenciamento de Rifas - Samaritanos")
        self.root.geometry("900x650")
        self.root.minsize(800, 600)
        self.root.configure(background=CORES["background"])
        
        self.rifa_manager = RifaManager()
        
        # Configuração do estilo
        self.configurar_estilo()
        
        # Criação do quadro principal
        self.main_frame = ttk.Frame(self.root, padding="10", style="Main.TFrame")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Cabeçalho com logo
        self.criar_cabecalho()
        
        # Barra de status na parte inferior - Movida para antes da criação das abas
        self.criar_barra_status()
        
        # Notebook para as diferentes funcionalidades
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Abas do notebook
        self.cadastro_frame = ttk.Frame(self.notebook, padding="10", style="Tab.TFrame")
        self.listagem_frame = ttk.Frame(self.notebook, padding="10", style="Tab.TFrame")
        self.busca_frame = ttk.Frame(self.notebook, padding="10", style="Tab.TFrame")
        self.exportar_frame = ttk.Frame(self.notebook, padding="10", style="Tab.TFrame")
        self.importar_frame = ttk.Frame(self.notebook, padding="10", style="Tab.TFrame")
        
        self.notebook.add(self.cadastro_frame, text=" Cadastro ")
        self.notebook.add(self.listagem_frame, text=" Listar Compradores ")
        self.notebook.add(self.busca_frame, text=" Buscar ")
        self.notebook.add(self.exportar_frame, text=" Exportar ")
        self.notebook.add(self.importar_frame, text=" Importar CSV ")
        
        # Configuração das abas
        self.setup_cadastro_tab()
        self.setup_listagem_tab()
        self.setup_busca_tab()
        self.setup_exportar_tab()
        self.setup_importar_tab()
        
        # Vincular eventos
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)
    
    def configurar_estilo(self):
        """Configura os estilos da aplicação"""
        self.style = ttk.Style()
        
        # Configurar cores do tema
        self.style.configure("TFrame", background=CORES["background"])
        self.style.configure("Main.TFrame", background=CORES["background"])
        self.style.configure("Tab.TFrame", background=CORES["background"])
        self.style.configure("Header.TFrame", background=CORES["primaria"])
        
        # Estilo para os labels
        self.style.configure("TLabel", background=CORES["background"], foreground=CORES["texto"])
        self.style.configure("Header.TLabel", font=("Arial", 16, "bold"), 
                             foreground=CORES["branco"], background=CORES["primaria"])
        self.style.configure("Subheader.TLabel", font=("Arial", 12, "bold"), 
                             foreground=CORES["primaria"])
        self.style.configure("Status.TLabel", background=CORES["primaria"], 
                             foreground=CORES["branco"], padding=5)
        
        # Estilo para os botões
        self.style.configure("TButton", font=("Arial", 10))
        self.style.configure("Primary.TButton", font=("Arial", 10, "bold"))
        
        # Estilo para frames com borda
        self.style.configure("Card.TFrame", relief="ridge", borderwidth=1)
        
        # Estilo para o notebook
        self.style.configure("TNotebook", background=CORES["background"], borderwidth=0)
        self.style.configure("TNotebook.Tab", background=CORES["secundaria"], 
                            foreground=CORES["branco"], font=("Arial", 10), padding=[10, 5])
        self.style.map("TNotebook.Tab",
                      background=[("selected", CORES["primaria"]), ("active", CORES["secundaria"])],
                      foreground=[("selected", CORES["branco"]), ("active", CORES["branco"])])
        
        # Estilo para o Treeview (tabelas)
        self.style.configure("Treeview", 
                            background=CORES["branco"],
                            foreground=CORES["texto"],
                            rowheight=25)
        self.style.configure("Treeview.Heading", 
                            font=('Arial', 10, 'bold'),
                            background=CORES["secundaria"],
                            foreground=CORES["branco"])
        self.style.map('Treeview', 
                      background=[('selected', CORES["secundaria"])],
                      foreground=[('selected', CORES["branco"])])
    
    def criar_cabecalho(self):
        """Cria o cabeçalho da aplicação com título"""
        self.header_frame = ttk.Frame(self.main_frame, style="Header.TFrame")
        self.header_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Título da aplicação
        self.title_label = ttk.Label(self.header_frame, 
                                    text="Sistema de Rifas Beneficentes - Samaritanos", 
                                    style="Header.TLabel")
        self.title_label.pack(side=tk.LEFT, padx=20, pady=10)
    
    def criar_barra_status(self):
        """Cria a barra de status na parte inferior da janela"""
        self.status_frame = ttk.Frame(self.root, style="Header.TFrame")
        self.status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        self.status_label = ttk.Label(self.status_frame, 
                                     text="Pronto", 
                                     style="Status.TLabel")
        self.status_label.pack(fill=tk.X)
    
    def atualizar_status(self, mensagem):
        """Atualiza a mensagem na barra de status"""
        self.status_label.config(text=mensagem)
    
    def on_tab_changed(self, event):
        """Função chamada quando a aba é alterada"""
        tab_id = self.notebook.select()
        tab_name = self.notebook.tab(tab_id, "text").strip()
        self.atualizar_status(f"Área: {tab_name}")
        
        # Se a aba de listagem for selecionada, atualizar a lista
        if "Listar" in tab_name:
            self.atualizar_listagem()
    
    def setup_cadastro_tab(self):
        # Título da aba
        ttk.Label(self.cadastro_frame, text="Cadastro de Números de Rifa", 
                 style="Subheader.TLabel").pack(pady=(0, 20))
        
        # Frame para cadastro com estilo de card
        self.cadastro_frame_inner = ttk.Frame(self.cadastro_frame, style="Card.TFrame", padding=20)
        self.cadastro_frame_inner.pack(fill=tk.X, pady=10, padx=20)
        
        # Grid para organizar os campos
        self.cadastro_frame_inner.columnconfigure(0, weight=1)
        self.cadastro_frame_inner.columnconfigure(1, weight=3)
        
        # Campos para cadastro
        ttk.Label(self.cadastro_frame_inner, text="Números (separados por vírgula):").grid(
            row=0, column=0, sticky=tk.W, pady=10, padx=5)
        self.numeros_entry = ttk.Entry(self.cadastro_frame_inner, width=40, font=("Arial", 11))
        self.numeros_entry.grid(row=0, column=1, sticky=tk.W+tk.E, pady=10, padx=5)
        
        ttk.Label(self.cadastro_frame_inner, text="Nome do Comprador:").grid(
            row=1, column=0, sticky=tk.W, pady=10, padx=5)
        self.nome_multi_entry = ttk.Entry(self.cadastro_frame_inner, width=40, font=("Arial", 11))
        self.nome_multi_entry.grid(row=1, column=1, sticky=tk.W+tk.E, pady=10, padx=5)
        
        ttk.Label(self.cadastro_frame_inner, text="Telefone:").grid(
            row=2, column=0, sticky=tk.W, pady=10, padx=5)
        self.telefone_multi_entry = ttk.Entry(self.cadastro_frame_inner, width=40, font=("Arial", 11))
        self.telefone_multi_entry.grid(row=2, column=1, sticky=tk.W+tk.E, pady=10, padx=5)
        
        # Frame para botões
        botoes_frame = ttk.Frame(self.cadastro_frame_inner, padding=(0, 10, 0, 0))
        botoes_frame.grid(row=3, column=0, columnspan=2, pady=15)
        
        # Botão de cadastro com estilo primário
        ttk.Button(botoes_frame, text="Cadastrar", style="Primary.TButton", 
                  command=self.cadastrar_multiplos, width=20).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(botoes_frame, text="Limpar Campos", 
                  command=self.limpar_campos_cadastro).pack(side=tk.LEFT, padx=5)
        
        # Instrução para cadastro
        info_frame = ttk.Frame(self.cadastro_frame, padding=(20, 15))
        info_frame.pack(fill=tk.X, pady=5)
        
        info_text = "• Para cadastrar um único número, insira apenas um número no campo acima.\n"
        info_text += "• Para cadastrar múltiplos números, separe-os por vírgula (ex: 10, 11, 12, 13)\n"
        info_text += "• Todos os campos são obrigatórios."
        
        info_label = ttk.Label(info_frame, text=info_text, wraplength=600, justify="left")
        info_label.pack(anchor=tk.W)
    
    def limpar_campos_cadastro(self):
        """Limpa os campos do formulário de cadastro"""
        self.numeros_entry.delete(0, tk.END)
        self.nome_multi_entry.delete(0, tk.END)
        self.telefone_multi_entry.delete(0, tk.END)
        self.numeros_entry.focus()
        
    def setup_listagem_tab(self):
        # Título da aba
        ttk.Label(self.listagem_frame, text="Listagem de Compradores", 
                 style="Subheader.TLabel").pack(pady=(0, 20))
        
        # Frame para controles
        controles_frame = ttk.Frame(self.listagem_frame)
        controles_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Botão para atualizar a listagem
        ttk.Button(controles_frame, text="Atualizar Listagem", 
                  command=self.atualizar_listagem).pack(side=tk.LEFT, padx=5)
        
        # Contador de registros
        self.contador_label = ttk.Label(controles_frame, text="Total: 0 registros")
        self.contador_label.pack(side=tk.RIGHT, padx=5)
        
        # Frame para a tabela
        tabela_frame = ttk.Frame(self.listagem_frame, style="Card.TFrame")
        tabela_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Treeview para exibir os compradores
        columns = ("numero", "nome", "telefone", "data_compra")
        self.tree = ttk.Treeview(tabela_frame, columns=columns, show="headings")
        
        # Configurando as colunas
        self.tree.heading("numero", text="Número")
        self.tree.heading("nome", text="Nome")
        self.tree.heading("telefone", text="Telefone")
        self.tree.heading("data_compra", text="Data da Compra")
        
        self.tree.column("numero", width=100)
        self.tree.column("nome", width=250)
        self.tree.column("telefone", width=150)
        self.tree.column("data_compra", width=180)
        
        # Adicionando scrollbars
        scrollbar_y = ttk.Scrollbar(tabela_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar_x = ttk.Scrollbar(tabela_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscroll=scrollbar_y.set, xscroll=scrollbar_x.set)
        
        # Posicionando os componentes
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Iniciar com a listagem atualizada
        self.atualizar_listagem()
        
    def setup_busca_tab(self):
        # Título da aba
        ttk.Label(self.busca_frame, text="Busca de Compradores", 
                 style="Subheader.TLabel").pack(pady=(0, 20))
        
        # Frame para as opções de busca
        opcoes_frame = ttk.Frame(self.busca_frame)
        opcoes_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Abas para as diferentes formas de busca
        busca_notebook = ttk.Notebook(opcoes_frame)
        busca_notebook.pack(fill=tk.X, pady=5)
        
        # Frame para busca por número
        self.busca_numero_frame = ttk.Frame(busca_notebook, padding=15, style="Card.TFrame")
        busca_notebook.add(self.busca_numero_frame, text="Busca por Número")
        
        # Organizando grid
        self.busca_numero_frame.columnconfigure(0, weight=1)
        self.busca_numero_frame.columnconfigure(1, weight=3)
        
        # Campos para busca por número
        ttk.Label(self.busca_numero_frame, text="Número da Rifa:").grid(
            row=0, column=0, sticky=tk.W, pady=10)
        self.busca_numero_entry = ttk.Entry(self.busca_numero_frame, width=15, font=("Arial", 11))
        self.busca_numero_entry.grid(row=0, column=1, sticky=tk.W, pady=10, padx=5)
        
        # Frame para botões
        botoes_numero_frame = ttk.Frame(self.busca_numero_frame)
        botoes_numero_frame.grid(row=1, column=0, columnspan=2, pady=10)
        
        ttk.Button(botoes_numero_frame, text="Buscar", style="Primary.TButton",
                  command=self.buscar_por_numero, width=15).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(botoes_numero_frame, text="Limpar", 
                  command=lambda: self.busca_numero_entry.delete(0, tk.END)).pack(side=tk.LEFT, padx=5)
        
        # Frame para busca por nome
        self.busca_nome_frame = ttk.Frame(busca_notebook, padding=15, style="Card.TFrame")
        busca_notebook.add(self.busca_nome_frame, text="Busca por Nome")
        
        # Organizando grid
        self.busca_nome_frame.columnconfigure(0, weight=1)
        self.busca_nome_frame.columnconfigure(1, weight=3)
        
        # Campos para busca por nome
        ttk.Label(self.busca_nome_frame, text="Nome (ou parte):").grid(
            row=0, column=0, sticky=tk.W, pady=10)
        self.busca_nome_entry = ttk.Entry(self.busca_nome_frame, width=30, font=("Arial", 11))
        self.busca_nome_entry.grid(row=0, column=1, sticky=tk.W+tk.E, pady=10, padx=5)
        
        # Frame para botões
        botoes_nome_frame = ttk.Frame(self.busca_nome_frame)
        botoes_nome_frame.grid(row=1, column=0, columnspan=2, pady=10)
        
        ttk.Button(botoes_nome_frame, text="Buscar", style="Primary.TButton",
                  command=self.buscar_por_nome, width=15).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(botoes_nome_frame, text="Limpar", 
                  command=lambda: self.busca_nome_entry.delete(0, tk.END)).pack(side=tk.LEFT, padx=5)
        
        # Frame para resultados
        resultado_label_frame = ttk.Frame(self.busca_frame)
        resultado_label_frame.pack(fill=tk.X, padx=20, pady=(20, 5))
        
        ttk.Label(resultado_label_frame, text="Resultados da Busca:", 
                 style="Subheader.TLabel").pack(side=tk.LEFT)
        
        self.resultado_contador = ttk.Label(resultado_label_frame, text="")
        self.resultado_contador.pack(side=tk.RIGHT)
        
        # Frame para a tabela de resultados
        resultados_frame = ttk.Frame(self.busca_frame, style="Card.TFrame")
        resultados_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=5)
        
        # Treeview para resultados
        columns = ("numero", "nome", "telefone", "data_compra")
        self.resultados_tree = ttk.Treeview(resultados_frame, columns=columns, show="headings")
        
        # Configurando as colunas
        self.resultados_tree.heading("numero", text="Número")
        self.resultados_tree.heading("nome", text="Nome")
        self.resultados_tree.heading("telefone", text="Telefone")
        self.resultados_tree.heading("data_compra", text="Data da Compra")
        
        self.resultados_tree.column("numero", width=100)
        self.resultados_tree.column("nome", width=250)
        self.resultados_tree.column("telefone", width=150)
        self.resultados_tree.column("data_compra", width=180)
        
        # Adicionando scrollbars
        scrollbar_y = ttk.Scrollbar(resultados_frame, orient=tk.VERTICAL, 
                                  command=self.resultados_tree.yview)
        scrollbar_x = ttk.Scrollbar(resultados_frame, orient=tk.HORIZONTAL, 
                                  command=self.resultados_tree.xview)
        self.resultados_tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        # Posicionando os componentes
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.resultados_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
    def setup_exportar_tab(self):
        # Título da aba
        ttk.Label(self.exportar_frame, text="Exportação de Dados", 
                 style="Subheader.TLabel").pack(pady=(0, 20))
        
        # Frame para exportação com estilo de card
        self.exportar_inner_frame = ttk.Frame(self.exportar_frame, style="Card.TFrame", padding=20)
        self.exportar_inner_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Texto explicativo
        ttk.Label(self.exportar_inner_frame, 
                 text="Exporte os dados para um arquivo CSV que pode ser aberto em Excel ou similares.",
                 wraplength=500, justify="center").pack(pady=10)
        
        ttk.Label(self.exportar_inner_frame, 
                 text="Esta função permite criar um backup dos seus dados ou compartilhá-los.",
                 wraplength=500, justify="center").pack(pady=5)
        
        # Botão de exportação
        ttk.Button(self.exportar_inner_frame, text="Escolher Local e Exportar", 
                  style="Primary.TButton", command=self.exportar_dados,
                  width=25).pack(pady=20)
        
        # Informações adicionais
        info_frame = ttk.Frame(self.exportar_frame, padding=10)
        info_frame.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Label(info_frame, text="Dicas:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(0, 5))
        
        tips = [
            "• Exporte regularmente como backup para evitar perda de dados",
            "• O arquivo CSV pode ser aberto no Excel, Google Sheets, LibreOffice, etc.",
            "• Para transferir dados entre computadores, use a exportação e importação"
        ]
        
        for tip in tips:
            ttk.Label(info_frame, text=tip, wraplength=600, justify="left").pack(anchor=tk.W, pady=2)
    
    def setup_importar_tab(self):
        # Título da aba
        ttk.Label(self.importar_frame, text="Importação de Dados", 
                 style="Subheader.TLabel").pack(pady=(0, 20))
        
        # Frame para importação com estilo de card
        self.importar_inner_frame = ttk.Frame(self.importar_frame, style="Card.TFrame", padding=20)
        self.importar_inner_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Texto explicativo
        ttk.Label(self.importar_inner_frame, 
                 text="Importe dados de um arquivo CSV externo para combinar com seus registros atuais.",
                 wraplength=500, justify="center").pack(pady=10)
        
        ttk.Label(self.importar_inner_frame, 
                 text="Números de rifa duplicados serão ignorados automaticamente.",
                 wraplength=500, justify="center").pack(pady=5)
        
        # Frame para exibir o caminho do arquivo
        file_frame = ttk.Frame(self.importar_inner_frame)
        file_frame.pack(fill=tk.X, pady=15)
        
        self.filepath_var = tk.StringVar()
        ttk.Label(file_frame, text="Arquivo:").pack(side=tk.LEFT, padx=5)
        ttk.Entry(file_frame, textvariable=self.filepath_var, width=50).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        ttk.Button(file_frame, text="Procurar...", command=self.escolher_arquivo_csv).pack(side=tk.LEFT, padx=5)
        
        # Botão para importar
        ttk.Button(self.importar_inner_frame, text="Importar Dados", 
                  style="Primary.TButton", command=self.importar_csv,
                  width=25).pack(pady=15)
        
        # Frame para resultados da importação
        resultado_label_frame = ttk.Frame(self.importar_frame)
        resultado_label_frame.pack(fill=tk.X, padx=20, pady=(20, 5))
        
        ttk.Label(resultado_label_frame, text="Resultado da Importação:", 
                 style="Subheader.TLabel").pack(side=tk.LEFT)
        
        # Frame para a área de texto de resultados
        self.resultado_frame = ttk.Frame(self.importar_frame, style="Card.TFrame")
        self.resultado_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=5)
        
        # Área de texto para mostrar resultados
        self.resultado_text = tk.Text(self.resultado_frame, height=10, wrap=tk.WORD,
                                    font=("Arial", 10), bg=CORES["branco"])
        
        # Scrollbar para a área de texto
        scrollbar = ttk.Scrollbar(self.resultado_frame, orient=tk.VERTICAL, command=self.resultado_text.yview)
        self.resultado_text.configure(yscrollcommand=scrollbar.set)
        
        # Posicionando os componentes
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.resultado_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    def cadastrar_multiplos(self):
        numeros_input = self.numeros_entry.get().strip()
        nome = self.nome_multi_entry.get().strip()
        telefone = self.telefone_multi_entry.get().strip()
        
        if not numeros_input or not nome or not telefone:
            messagebox.showerror("Erro", "Todos os campos são obrigatórios!")
            return
        
        numeros = [num.strip() for num in numeros_input.split(',')]
        
        # Se for apenas um número, usar a função de cadastro único
        if len(numeros) == 1:
            sucesso, mensagem = self.rifa_manager.cadastrar_comprador(numeros[0], nome, telefone)
        else:
            sucesso, mensagem = self.rifa_manager.cadastrar_multiplos_numeros(numeros, nome, telefone)
        
        if sucesso:
            messagebox.showinfo("Sucesso", mensagem)
            self.limpar_campos_cadastro()
            self.atualizar_status(f"Cadastro realizado: {len(numeros)} número(s) para {nome}")
            self.atualizar_listagem()
        else:
            messagebox.showwarning("Atenção", mensagem)
    
    def atualizar_listagem(self):
        # Limpar treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Adicionar dados
        compradores = self.rifa_manager.listar_compradores()
        for comprador in compradores:
            self.tree.insert("", tk.END, values=(
                comprador['numero'],
                comprador['nome'],
                comprador['telefone'],
                comprador['data_compra']
            ))
            
        # Atualizar contador
        total = len(compradores)
        self.contador_label.config(text=f"Total: {total} registro{'s' if total != 1 else ''}")
        self.atualizar_status(f"Listagem atualizada: {total} registro{'s' if total != 1 else ''}")
    
    def buscar_por_numero(self):
        numero = self.busca_numero_entry.get().strip()
        
        if not numero:
            messagebox.showerror("Erro", "Digite um número para buscar!")
            return
        
        comprador = self.rifa_manager.buscar_por_numero(numero)
        
        # Limpar resultados anteriores
        for item in self.resultados_tree.get_children():
            self.resultados_tree.delete(item)
        
        if comprador:
            self.resultados_tree.insert("", tk.END, values=(
                comprador['numero'],
                comprador['nome'],
                comprador['telefone'],
                comprador['data_compra']
            ))
            self.resultado_contador.config(text="1 resultado encontrado")
            self.atualizar_status(f"Busca por número: encontrado número {numero}")
        else:
            messagebox.showinfo("Busca", f"Nenhum comprador encontrado com o número {numero}.")
            self.resultado_contador.config(text="0 resultados")
            self.atualizar_status(f"Busca por número: nenhum resultado para {numero}")
    
    def buscar_por_nome(self):
        nome = self.busca_nome_entry.get().strip()
        
        if not nome:
            messagebox.showerror("Erro", "Digite um nome para buscar!")
            return
        
        resultados = self.rifa_manager.buscar_por_nome(nome)
        
        # Limpar resultados anteriores
        for item in self.resultados_tree.get_children():
            self.resultados_tree.delete(item)
        
        if resultados:
            for r in resultados:
                self.resultados_tree.insert("", tk.END, values=(
                    r['numero'],
                    r['nome'],
                    r['telefone'],
                    r['data_compra']
                ))
            total = len(resultados)
            self.resultado_contador.config(text=f"{total} resultado{'s' if total != 1 else ''} encontrado{'s' if total != 1 else ''}")
            self.atualizar_status(f"Busca por nome: {total} resultado{'s' if total != 1 else ''} para '{nome}'")
        else:
            messagebox.showinfo("Busca", f"Nenhum comprador encontrado com o nome '{nome}'.")
            self.resultado_contador.config(text="0 resultados")
            self.atualizar_status(f"Busca por nome: nenhum resultado para '{nome}'")
    
    def exportar_dados(self):
        arquivo_destino = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")],
            title="Salvar dados como..."
        )
        
        if arquivo_destino:
            sucesso, mensagem = self.rifa_manager.exportar_para_csv(arquivo_destino)
            if sucesso:
                messagebox.showinfo("Exportação", mensagem)
                self.atualizar_status(f"Dados exportados para {os.path.basename(arquivo_destino)}")
            else:
                messagebox.showerror("Erro", mensagem)
                self.atualizar_status("Erro na exportação de dados")
    
    def escolher_arquivo_csv(self):
        arquivo = filedialog.askopenfilename(
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")],
            title="Selecionar arquivo CSV para importação"
        )
        
        if arquivo:
            self.filepath_var.set(arquivo)
            self.atualizar_status(f"Arquivo selecionado: {os.path.basename(arquivo)}")
    
    def importar_csv(self):
        arquivo_origem = self.filepath_var.get().strip()
        
        if not arquivo_origem:
            messagebox.showerror("Erro", "Selecione um arquivo CSV para importar!")
            return
        
        if not os.path.exists(arquivo_origem):
            messagebox.showerror("Erro", f"O arquivo {arquivo_origem} não foi encontrado!")
            return
        
        # Limpar área de resultados
        self.resultado_text.delete(1.0, tk.END)
        
        # Configurar tags para formatação de texto
        self.resultado_text.tag_configure("titulo", font=("Arial", 10, "bold"))
        self.resultado_text.tag_configure("sucesso", foreground=CORES["sucesso"])
        self.resultado_text.tag_configure("erro", foreground=CORES["erro"])
        self.resultado_text.tag_configure("aviso", foreground=CORES["aviso"])
        
        # Executar a importação
        sucesso, mensagem, stats = merge_csv_files(arquivo_origem=arquivo_origem)
        
        # Exibir resultados
        self.resultado_text.insert(tk.END, mensagem + "\n\n", "titulo")
        
        if sucesso:
            if stats['total_adicionados'] > 0:
                self.resultado_text.insert(tk.END, "Números adicionados:\n", "sucesso")
                for num in stats['numeros_adicionados']:
                    self.resultado_text.insert(tk.END, f" - {num}\n")
            
            if stats['total_ignorados'] > 0:
                self.resultado_text.insert(tk.END, "\nNúmeros ignorados (já existentes):\n", "aviso")
                for num in stats['numeros_ignorados']:
                    self.resultado_text.insert(tk.END, f" - {num}\n")
            
            # Atualizar a lista de compradores após a importação
            self.atualizar_listagem()
            
            messagebox.showinfo("Importação", "Importação concluída com sucesso!")
            self.atualizar_status(f"Importação concluída: {stats['total_adicionados']} adicionados, {stats['total_ignorados']} ignorados")
        else:
            self.resultado_text.insert(tk.END, "Erro na importação!\n", "erro")
            self.resultado_text.insert(tk.END, mensagem)
            messagebox.showerror("Erro", mensagem)
            self.atualizar_status("Erro na importação de dados")

def main():
    root = tk.Tk()
    app = RifaGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
