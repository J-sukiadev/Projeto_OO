import tkinter as tk
from tkinter import ttk, messagebox

class HabitatsView:
    def __init__(self, parent, habitat_service):
        self.parent = parent
        self.habitat_service = habitat_service
        self.setup_ui()
    
    def setup_ui(self):
        # Frame de cabeçalho
        header_frame = ttk.Frame(self.parent)
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(header_frame, text="Gerenciamento de Habitats", style='Header.TLabel').pack(side=tk.LEFT)
        
        # Botão de adicionar
        add_btn = ttk.Button(header_frame, text="+ Adicionar Habitat", command=self.show_add_dialog)
        add_btn.pack(side=tk.RIGHT)
        
        # Treeview
        self.tree = ttk.Treeview(
            self.parent,
            columns=('nome', 'tipo', 'capacidade', 'animais', 'vagas'),
            show='headings'
        )
        
        # Configuração das colunas
        columns = [
            ('nome', 'Nome', 150),
            ('tipo', 'Tipo', 100),
            ('capacidade', 'Capacidade', 80),
            ('animais', 'Animais', 80),
            ('vagas', 'Vagas', 80)
        ]
        
        for col_id, heading, width in columns:
            self.tree.heading(col_id, text=heading)
            self.tree.column(col_id, width=width)
        
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Botão de atualizar
        btn_frame = ttk.Frame(self.parent)
        btn_frame.pack(fill=tk.X, padx=10, pady=10)
        ttk.Button(btn_frame, text="Atualizar", command=self.load_data).pack(side=tk.RIGHT)
        
        self.load_data()
    
    def load_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        habitats = self.habitat_service.listar_habitats()
        for habitat in habitats:
            self.tree.insert('', tk.END, values=(
                habitat['nome'],
                habitat['tipo'],
                habitat['capacidade'],
                len(habitat['animais']),
                habitat['vagas']
            ))
    
    def show_add_dialog(self):
        dialog = tk.Toplevel(self.parent)
        dialog.title("Adicionar Habitat")
        dialog.geometry("300x250")
        dialog.resizable(False, False)
        
        # Variáveis do formulário
        self.nome_var = tk.StringVar()
        self.tipo_var = tk.StringVar()
        self.capacidade_var = tk.StringVar()
        
        # Formulário
        form_frame = ttk.Frame(dialog, padding=10)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # Campos
        campos = [
            ("Nome:", self.nome_var),
            ("Tipo:", self.tipo_var),
            ("Capacidade:", self.capacidade_var)
        ]
        
        for i, (label, var) in enumerate(campos):
            ttk.Label(form_frame, text=label).grid(row=i, column=0, sticky=tk.W, pady=5)
            
            if label == "Tipo:":
                ttk.Combobox(form_frame, textvariable=var, 
                            values=['Savana', 'Floresta', 'Aquático', 'Deserto', 'Polar']).grid(row=i, column=1, sticky=tk.EW, pady=5)
            else:
                ttk.Entry(form_frame, textvariable=var).grid(row=i, column=1, sticky=tk.EW, pady=5)
        
        # Botões
        btn_frame = ttk.Frame(dialog, padding=10)
        btn_frame.pack(fill=tk.X)
        
        ttk.Button(btn_frame, text="Cancelar", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Salvar", command=lambda: self.salvar_habitat(dialog)).pack(side=tk.RIGHT, padx=5)
    
    def salvar_habitat(self, dialog):
        dados = {
            'nome': self.nome_var.get(),
            'tipo': self.tipo_var.get(),
            'capacidade': self.capacidade_var.get()
        }
        
        resultado = self.habitat_service.criar_habitat(dados)
        if resultado['sucesso']:
            messagebox.showinfo("Sucesso", "Habitat criado com sucesso!")
            self.load_data()
            dialog.destroy()
        else:
            messagebox.showerror("Erro", resultado['mensagem'])