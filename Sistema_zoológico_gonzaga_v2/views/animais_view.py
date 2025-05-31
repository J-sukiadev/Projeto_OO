import tkinter as tk
from tkinter import ttk, messagebox
from package.models.animal import Mamifero, Ave, Reptil

class AnimaisView:
    def __init__(self, parent, animal_service):
        self.parent = parent
        self.animal_service = animal_service
        self.animal_selecionado = None
        self.setup_ui()
    
    def setup_ui(self):
        # Frame de cabeçalho
        header_frame = ttk.Frame(self.parent)
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(header_frame, text="Gerenciamento de Animais", style='Header.TLabel').pack(side=tk.LEFT)
        
        # Botão de adicionar
        add_btn = ttk.Button(header_frame, text="+ Adicionar Animal", command=self.show_formulario)
        add_btn.pack(side=tk.RIGHT)
        
        # Treeview
        self.tree_frame = ttk.Frame(self.parent)
        self.tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.tree = ttk.Treeview(
            self.tree_frame,
            columns=('nome', 'especie', 'idade', 'tipo', 'habitat'),
            show='headings'
        )
        
        # Configuração das colunas
        columns = [
            ('nome', 'Nome', 150),
            ('especie', 'Espécie', 150),
            ('idade', 'Idade', 80),
            ('tipo', 'Tipo', 100),
            ('habitat', 'Habitat', 120)
        ]
        
        for col_id, heading, width in columns:
            self.tree.heading(col_id, text=heading)
            self.tree.column(col_id, width=width)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Botões de ação
        btn_frame = ttk.Frame(self.parent)
        btn_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(btn_frame, text="Editar", command=self.editar_animal).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Remover", command=self.remover_animal).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Atualizar", command=self.load_data).pack(side=tk.RIGHT, padx=5)
        
        self.load_data()
    
    def load_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        animais = self.animal_service.listar_animais()
        for animal in animais:
            self.tree.insert('', tk.END, values=(
                animal['nome'],
                animal['especie'],
                animal['idade'],
                animal['tipo'],
                animal['habitat']
            ))

        # Atualiza o título com a contagem
        self.tree.heading('nome', text=f"Nome ({len(animais)})")

    def show_formulario(self, animal=None):
        self.animal_selecionado = animal
        dialog = tk.Toplevel(self.parent)
        dialog.title("Editar Animal" if animal else "Adicionar Animal")
        dialog.geometry("400x450")
        dialog.resizable(False, False)
        
        # Variáveis do formulário
        self.nome_var = tk.StringVar(value=animal['nome'] if animal else '')
        self.especie_var = tk.StringVar(value=animal['especie'] if animal else '')
        self.idade_var = tk.StringVar(value=animal['idade'] if animal else '')
        self.tipo_var = tk.StringVar(value=animal['tipo'] if animal else 'Mamifero')
        self.habitat_var = tk.StringVar(value=animal['habitat'] if animal else '')
        
        # Carrega detalhes específicos
        if animal:
            if animal['tipo'] == 'Mamifero':
                self.pelagem_var = tk.StringVar(value=animal.get('pelagem', 'curta'))
            elif animal['tipo'] == 'Ave':
                self.envergadura_var = tk.StringVar(value=animal.get('envergadura', 1.0))
            else:
                self.escamas_var = tk.StringVar(value=animal.get('escamas', 'escamosas'))
        else:
            self.pelagem_var = tk.StringVar(value='curta')
            self.envergadura_var = tk.StringVar(value='1.0')
            self.escamas_var = tk.StringVar(value='escamosas')
        
        # Frame principal
        form_frame = ttk.Frame(dialog, padding=10)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # Campos comuns
        campos_comuns = [
            ("Nome:", self.nome_var),
            ("Espécie:", self.especie_var),
            ("Idade:", self.idade_var),
            ("Habitat:", self.habitat_var)
        ]
        
        for i, (label, var) in enumerate(campos_comuns):
            ttk.Label(form_frame, text=label).grid(row=i, column=0, sticky=tk.W, pady=5)
            ttk.Entry(form_frame, textvariable=var).grid(row=i, column=1, sticky=tk.EW, pady=5)
        
        # Tipo de animal
        ttk.Label(form_frame, text="Tipo:").grid(row=4, column=0, sticky=tk.W, pady=5)
        tipo_cb = ttk.Combobox(form_frame, textvariable=self.tipo_var, 
                             values=['Mamifero', 'Ave', 'Reptil'], 
                             state='readonly')
        tipo_cb.grid(row=4, column=1, sticky=tk.EW, pady=5)
        tipo_cb.bind('<<ComboboxSelected>>', self.atualizar_campos_especificos)
        
        # Frame para campos específicos
        self.specific_frame = ttk.Frame(form_frame)
        self.specific_frame.grid(row=5, column=0, columnspan=2, sticky=tk.EW, pady=5)
        self.atualizar_campos_especificos()
        
        # Botões
        btn_frame = ttk.Frame(dialog, padding=10)
        btn_frame.pack(fill=tk.X)
        
        ttk.Button(btn_frame, text="Cancelar", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Salvar", command=lambda: self.salvar_animal(dialog)).pack(side=tk.RIGHT, padx=5)
    
    def atualizar_campos_especificos(self, event=None):
        for widget in self.specific_frame.winfo_children():
            widget.destroy()
        
        tipo = self.tipo_var.get()
        
        if tipo == 'Mamifero':
            ttk.Label(self.specific_frame, text="Pelagem:").grid(row=0, column=0, sticky=tk.W, pady=5)
            ttk.Entry(self.specific_frame, textvariable=self.pelagem_var).grid(row=0, column=1, sticky=tk.EW, pady=5)
        elif tipo == 'Ave':
            ttk.Label(self.specific_frame, text="Envergadura:").grid(row=0, column=0, sticky=tk.W, pady=5)
            ttk.Entry(self.specific_frame, textvariable=self.envergadura_var).grid(row=0, column=1, sticky=tk.EW, pady=5)
        else:  # Réptil
            ttk.Label(self.specific_frame, text="Escamas:").grid(row=0, column=0, sticky=tk.W, pady=5)
            ttk.Entry(self.specific_frame, textvariable=self.escamas_var).grid(row=0, column=1, sticky=tk.EW, pady=5)
    
    def salvar_animal(self, dialog):
        dados = {
            'nome': self.nome_var.get(),
            'especie': self.especie_var.get(),
            'idade': self.idade_var.get(),
            'tipo': self.tipo_var.get(),
            'habitat': self.habitat_var.get()
        }
        
        # Adiciona campos específicos
        if dados['tipo'] == 'Mamifero':
            dados['pelagem'] = self.pelagem_var.get()
        elif dados['tipo'] == 'Ave':
            dados['envergadura'] = self.envergadura_var.get()
        else:
            dados['escamas'] = self.escamas_var.get()
        
        if self.animal_selecionado:
            # Modo edição
            resultado = self.animal_service.editar_animal(self.animal_selecionado['nome'], dados)
            mensagem_sucesso = "Animal atualizado com sucesso!"
        else:
            # Modo adição
            resultado = self.animal_service.cadastrar_animal(dados)
            mensagem_sucesso = "Animal cadastrado com sucesso!"
        
        if resultado['sucesso']:
            messagebox.showinfo("Sucesso", mensagem_sucesso)
            self.load_data()
            dialog.destroy()
        else:
            messagebox.showerror("Erro", resultado['mensagem'])
    
    def editar_animal(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione um animal para editar")
            return
        
        # Obtém os dados do animal selecionado
        item = self.tree.item(selected[0])
        valores = item['values']
        
        animal = {
            'nome': valores[0],
            'especie': valores[1],
            'idade': valores[2],
            'tipo': valores[3],
            'habitat': valores[4]
        }
        
        # Carrega detalhes adicionais do serviço
        detalhes = self.animal_service.obter_detalhes_animal(valores[0])
        if detalhes:
            animal.update(detalhes)
        
        self.show_formulario(animal)
    
    def remover_animal(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione um animal para remover")
            return
        
        nome = self.tree.item(selected[0])['values'][0]
        if messagebox.askyesno("Confirmar", f"Remover o animal {nome} permanentemente?"):
            resultado = self.animal_service.remover_animal(nome)
            
            if resultado['sucesso']:
                messagebox.showinfo("Sucesso", resultado['mensagem'])
                self.load_data()
            else:
                messagebox.showerror("Erro", resultado['mensagem'])