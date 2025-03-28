import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
from rifa_manager import RifaManager
from csv_merger import merge_csv_files

class RifaGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gerenciamento de Rifas")
        self.root.geometry("800x600")
        self.rifa_manager = RifaManager()
        
        # Configuração do estilo
        self.style = ttk.Style()
        self.style.configure("TFrame", background="#f0f0f0")
        self.style.configure("TButton", font=("Arial", 10))
        self.style.configure("TLabel", font=("Arial", 10), background="#f0f0f0")
        self.style.configure("Header.TLabel", font=("Arial", 14, "bold"), background="#f0f0f0")
        
        # Criação do quadro principal
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        self.title_label = ttk.Label(self.main_frame, text="Sistema de Gerenciamento de Rifas", 
                                     style="Header.TLabel")
        self.title_label.pack(pady=(0, 20))
        
        # Notebook para as diferentes funcionalidades
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Abas do notebook
        self.cadastro_frame = ttk.Frame(self.notebook, padding="10")
        self.listagem_frame = ttk.Frame(self.notebook, padding="10")
        self.busca_frame = ttk.Frame(self.notebook, padding="10")
        self.exportar_frame = ttk.Frame(self.notebook, padding="10")
        self.importar_frame = ttk.Frame(self.notebook, padding="10")  # Nova aba para importação
        
        self.notebook.add(self.cadastro_frame, text="Cadastro")
        self.notebook.add(self.listagem_frame, text="Listar Compradores")
        self.notebook.add(self.busca_frame, text="Buscar")
        self.notebook.add(self.exportar_frame, text="Exportar")
        self.notebook.add(self.importar_frame, text="Importar CSV")  # Adicionar a nova aba
        
        # Configuração das abas
        self.setup_cadastro_tab()
        self.setup_listagem_tab()
        self.setup_busca_tab()
        self.setup_exportar_tab()
        self.setup_importar_tab()  # Configurar a nova aba
    
    def setup_cadastro_tab(self):
        # Frame para cadastro
        self.cadastro_frame_inner = ttk.LabelFrame(self.cadastro_frame, text="Cadastro", padding="10")
        self.cadastro_frame_inner.pack(fill=tk.X, pady=10)
        
        # Campos para cadastro
        ttk.Label(self.cadastro_frame_inner, text="Números (separados por vírgula):").grid(
            row=0, column=0, sticky=tk.W, pady=5)
        self.numeros_entry = ttk.Entry(self.cadastro_frame_inner, width=30)
        self.numeros_entry.grid(row=0, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(self.cadastro_frame_inner, text="Nome do Comprador:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.nome_multi_entry = ttk.Entry(self.cadastro_frame_inner, width=30)
        self.nome_multi_entry.grid(row=1, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(self.cadastro_frame_inner, text="Telefone:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.telefone_multi_entry = ttk.Entry(self.cadastro_frame_inner, width=20)
        self.telefone_multi_entry.grid(row=2, column=1, sticky=tk.W, pady=5)
        
        ttk.Button(self.cadastro_frame_inner, text="Cadastrar", 
                   command=self.cadastrar_multiplos).grid(row=3, column=0, columnspan=2, pady=10)
        
        # Instrução para cadastro único
        ttk.Label(self.cadastro_frame_inner, 
                 text="Para cadastrar um único número, insira apenas um número no campo acima.").grid(
            row=4, column=0, columnspan=2, sticky=tk.W, pady=(10, 0))
        
    def setup_listagem_tab(self):
        # Frame para a lista de compradores
        self.listagem_inner_frame = ttk.Frame(self.listagem_frame, padding="10")
        self.listagem_inner_frame.pack(fill=tk.BOTH, expand=True)
        
        # Botão para atualizar a listagem
        ttk.Button(self.listagem_inner_frame, text="Atualizar Listagem", 
                   command=self.atualizar_listagem).pack(pady=(0, 10))
        
        # Treeview para exibir os compradores
        columns = ("numero", "nome", "telefone", "data_compra")
        self.tree = ttk.Treeview(self.listagem_inner_frame, columns=columns, show="headings")
        
        # Configurando as colunas
        self.tree.heading("numero", text="Número")
        self.tree.heading("nome", text="Nome")
        self.tree.heading("telefone", text="Telefone")
        self.tree.heading("data_compra", text="Data da Compra")
        
        self.tree.column("numero", width=70)
        self.tree.column("nome", width=200)
        self.tree.column("telefone", width=150)
        self.tree.column("data_compra", width=150)
        
        # Adicionando scrollbar
        scrollbar = ttk.Scrollbar(self.listagem_inner_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        # Posicionando os componentes
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Iniciar com a listagem atualizada
        self.atualizar_listagem()
        
    def setup_busca_tab(self):
        # Frame para busca por número
        self.busca_numero_frame = ttk.LabelFrame(self.busca_frame, text="Busca por Número", padding="10")
        self.busca_numero_frame.pack(fill=tk.X, pady=10)
        
        # Campos para busca por número
        ttk.Label(self.busca_numero_frame, text="Número da Rifa:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.busca_numero_entry = ttk.Entry(self.busca_numero_frame, width=10)
        self.busca_numero_entry.grid(row=0, column=1, sticky=tk.W, pady=5)
        
        ttk.Button(self.busca_numero_frame, text="Buscar", 
                   command=self.buscar_por_numero).grid(row=0, column=2, padx=5, pady=5)
        
        # Frame para busca por nome
        self.busca_nome_frame = ttk.LabelFrame(self.busca_frame, text="Busca por Nome", padding="10")
        self.busca_nome_frame.pack(fill=tk.X, pady=10)
        
        # Campos para busca por nome
        ttk.Label(self.busca_nome_frame, text="Nome (ou parte):").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.busca_nome_entry = ttk.Entry(self.busca_nome_frame, width=20)
        self.busca_nome_entry.grid(row=0, column=1, sticky=tk.W, pady=5)
        
        ttk.Button(self.busca_nome_frame, text="Buscar", 
                   command=self.buscar_por_nome).grid(row=0, column=2, padx=5, pady=5)
        
        # Frame para resultados
        self.resultados_frame = ttk.LabelFrame(self.busca_frame, text="Resultados", padding="10")
        self.resultados_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Treeview para resultados
        columns = ("numero", "nome", "telefone", "data_compra")
        self.resultados_tree = ttk.Treeview(self.resultados_frame, columns=columns, show="headings")
        
        # Configurando as colunas
        self.resultados_tree.heading("numero", text="Número")
        self.resultados_tree.heading("nome", text="Nome")
        self.resultados_tree.heading("telefone", text="Telefone")
        self.resultados_tree.heading("data_compra", text="Data da Compra")
        
        self.resultados_tree.column("numero", width=70)
        self.resultados_tree.column("nome", width=200)
        self.resultados_tree.column("telefone", width=150)
        self.resultados_tree.column("data_compra", width=150)
        
        # Adicionando scrollbar
        scrollbar = ttk.Scrollbar(self.resultados_frame, orient=tk.VERTICAL, 
                                  command=self.resultados_tree.yview)
        self.resultados_tree.configure(yscrollcommand=scrollbar.set)
        
        # Posicionando os componentes
        self.resultados_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
    def setup_exportar_tab(self):
        # Frame para exportação
        self.exportar_inner_frame = ttk.Frame(self.exportar_frame, padding="10")
        self.exportar_inner_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(self.exportar_inner_frame, 
                  text="Exporte os dados para um arquivo CSV").pack(pady=10)
        
        ttk.Button(self.exportar_inner_frame, text="Escolher Local e Exportar", 
                   command=self.exportar_dados).pack(pady=10)
    
    def setup_importar_tab(self):
        # Frame para importação
        self.importar_inner_frame = ttk.Frame(self.importar_frame, padding="10")
        self.importar_inner_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(self.importar_inner_frame, 
                  text="Importe dados de um arquivo CSV externo").pack(pady=10)
        
        ttk.Label(self.importar_inner_frame, 
                  text="Números de rifa duplicados serão ignorados.").pack(pady=2)
        
        # Frame para exibir o caminho do arquivo
        file_frame = ttk.Frame(self.importar_inner_frame)
        file_frame.pack(fill=tk.X, pady=10)
        
        self.filepath_var = tk.StringVar()
        ttk.Label(file_frame, text="Arquivo:").pack(side=tk.LEFT, padx=5)
        ttk.Entry(file_frame, textvariable=self.filepath_var, width=50).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        ttk.Button(file_frame, text="Procurar...", command=self.escolher_arquivo_csv).pack(side=tk.LEFT, padx=5)
        
        # Botão para importar
        ttk.Button(self.importar_inner_frame, text="Importar Dados", 
                   command=self.importar_csv).pack(pady=10)
        
        # Frame para resultados da importação
        self.resultado_frame = ttk.LabelFrame(self.importar_inner_frame, text="Resultado da Importação", padding="10")
        self.resultado_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Área de texto para mostrar resultados
        self.resultado_text = tk.Text(self.resultado_frame, height=10, wrap=tk.WORD)
        self.resultado_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Scrollbar para a área de texto
        scrollbar = ttk.Scrollbar(self.resultado_frame, orient=tk.VERTICAL, command=self.resultado_text.yview)
        self.resultado_text.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def cadastrar_comprador(self):
        # Esta função não é mais chamada diretamente, mas mantida por compatibilidade
        pass
    
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
            self.numeros_entry.delete(0, tk.END)
            self.nome_multi_entry.delete(0, tk.END)
            self.telefone_multi_entry.delete(0, tk.END)
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
        else:
            messagebox.showinfo("Busca", f"Nenhum comprador encontrado com o número {numero}.")
    
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
        else:
            messagebox.showinfo("Busca", f"Nenhum comprador encontrado com o nome '{nome}'.")
    
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
            else:
                messagebox.showerror("Erro", mensagem)
    
    def escolher_arquivo_csv(self):
        arquivo = filedialog.askopenfilename(
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")],
            title="Selecionar arquivo CSV para importação"
        )
        
        if arquivo:
            self.filepath_var.set(arquivo)
    
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
        
        # Executar a importação
        sucesso, mensagem, stats = merge_csv_files(arquivo_origem=arquivo_origem)
        
        # Exibir resultados
        self.resultado_text.insert(tk.END, mensagem + "\n\n")
        
        if sucesso:
            if stats['total_adicionados'] > 0:
                self.resultado_text.insert(tk.END, "Números adicionados:\n")
                for num in stats['numeros_adicionados']:
                    self.resultado_text.insert(tk.END, f" - {num}\n")
            
            if stats['total_ignorados'] > 0:
                self.resultado_text.insert(tk.END, "\nNúmeros ignorados (já existentes):\n")
                for num in stats['numeros_ignorados']:
                    self.resultado_text.insert(tk.END, f" - {num}\n")
            
            # Atualizar a lista de compradores após a importação
            self.atualizar_listagem()
            
            messagebox.showinfo("Importação", "Importação concluída com sucesso!")
        else:
            messagebox.showerror("Erro", mensagem)

def main():
    root = tk.Tk()
    app = RifaGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
