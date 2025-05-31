import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class VisitantesView:
    def __init__(self, parent, visita_service):
        self.parent = parent
        self.visita_service = visita_service
        self.setup_ui()
    
    def setup_ui(self):
        # Frame de cabeçalho
        header_frame = ttk.Frame(self.parent)
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(header_frame, text="Gerenciamento de Visitantes", style='Header.TLabel').pack(side=tk.LEFT)
        
        # Botão de registrar visita
        add_btn = ttk.Button(header_frame, text="+ Registrar Visita", command=self.show_registro_dialog)
        add_btn.pack(side=tk.RIGHT)
        
        # Treeview
        self.tree = ttk.Treeview(
            self.parent,
            columns=('nome', 'idade', 'ingressos'),
            show='headings'
        )
        
        # Configuração das colunas
        columns = [
            ('nome', 'Nome', 200),
            ('idade', 'Idade', 80),
            ('ingressos', 'Ingressos', 80)
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
            
        visitantes = self.visita_service.listar_visitantes()
        for visitante in visitantes:
            self.tree.insert('', tk.END, values=(
                visitante['nome'],
                visitante['idade'],
                visitante['ingressos']
            ))
    
    def show_registro_dialog(self):
        dialog = tk.Toplevel(self.parent)
        dialog.title("Registrar Nova Visita")
        dialog.geometry("300x200")
        dialog.resizable(False, False)
        
        # Variáveis do formulário
        self.nome_var = tk.StringVar()
        self.idade_var = tk.StringVar()
        
        # Formulário
        form_frame = ttk.Frame(dialog, padding=10)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # Campos
        campos = [
            ("Nome:", self.nome_var),
            ("Idade:", self.idade_var)
        ]
        
        for i, (label, var) in enumerate(campos):
            ttk.Label(form_frame, text=label).grid(row=i, column=0, sticky=tk.W, pady=5)
            ttk.Entry(form_frame, textvariable=var).grid(row=i, column=1, sticky=tk.EW, pady=5)
        
        # Botões
        btn_frame = ttk.Frame(dialog, padding=10)
        btn_frame.pack(fill=tk.X)
        
        ttk.Button(btn_frame, text="Cancelar", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Registrar", command=lambda: self.registrar_visita(dialog)).pack(side=tk.RIGHT, padx=5)
    
    def registrar_visita(self, dialog):
        dados = {
            'nome': self.nome_var.get(),
            'idade': self.idade_var.get()
        }
        
        resultado = self.visita_service.registrar_visita(dados)
        if resultado['sucesso']:
            messagebox.showinfo("Sucesso", 
                f"Visita registrada!\nIngresso: {resultado['ingresso']['codigo']}\n"
                f"Valor: R${resultado['ingresso']['valor']:.2f}")
            self.load_data()
            dialog.destroy()
        else:
            messagebox.showerror("Erro", resultado['mensagem'])