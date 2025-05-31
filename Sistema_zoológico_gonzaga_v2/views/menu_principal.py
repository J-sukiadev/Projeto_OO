import tkinter as tk
from tkinter import ttk
from . import animais_view, habitats_view, visitantes_view, relatorios_view
from package.services import AnimalService, HabitatService, VisitaService


class MenuPrincipal:
    def __init__(self, root, zoo, logger):
        self.root = root
        self.zoo = zoo
        self.logger = logger
        self._inicializar_servicos()
        self.setup_ui()
    
    def _inicializar_servicos(self):
        """Inicializa todos os serviços necessários"""
        self.animal_service = AnimalService(self.zoo, self.logger)
        self.habitat_service = HabitatService(self.zoo, self.logger)
        self.visita_service = VisitaService(self.zoo, self.logger)
        self.salvar_estado()
    
    def setup_ui(self):
        # Frame principal
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Barra lateral
        self.sidebar = ttk.Frame(self.main_frame, width=200, style='Sidebar.TFrame')
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)
        
        # Conteúdo principal
        self.content = ttk.Frame(self.main_frame)
        self.content.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Adicionar botões na sidebar
        self.add_sidebar_buttons()
        
        # Configurar estilo da sidebar
        style = ttk.Style()
        style.configure('Sidebar.TFrame', background='#2c3e50')
        
        # Exibir dashboard inicial
        self.show_dashboard()
    
    def add_sidebar_buttons(self):
        buttons = [
            ("Dashboard", self.show_dashboard),
            ("Animais", self.show_animais),
            ("Habitats", self.show_habitats),
            ("Visitantes", self.show_visitantes),
            ("Relatórios", self.show_relatorios),
            ("Sair", self.sair)
        ]
        
        for text, command in buttons:
            btn = ttk.Button(
                self.sidebar, 
                text=text, 
                command=command,
                style='Sidebar.TButton'
            )
            btn.pack(fill=tk.X, padx=5, pady=5)
        
        style = ttk.Style()
        style.configure('Sidebar.TButton', 
                      foreground='white', 
                      background='#34495e', 
                      borderwidth=0, 
                      font=('Arial', 11))
        style.map('Sidebar.TButton',
                background=[('active', '#2980b9')])
    
    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()
    
    def show_dashboard(self):
        self.clear_content()
        ttk.Label(self.content, text="Dashboard - Visão Geral", style='Header.TLabel').pack(pady=20)
        
        # Widgets do dashboard
        frame_stats = ttk.Frame(self.content)
        frame_stats.pack(pady=10)
        
        # Estatísticas rápidas
        stats = [
            ("Animais", len(self.zoo.animais)),
            ("Habitats", len(self.zoo.habitats)),
            ("Visitantes", len(self.zoo.visitantes))
        ]
        
        for text, value in stats:
            frame = ttk.Frame(frame_stats)
            frame.pack(side=tk.LEFT, padx=10)
            ttk.Label(frame, text=text, font=('Arial', 10)).pack()
            ttk.Label(frame, text=str(value), font=('Arial', 14, 'bold')).pack()
    
    def show_animais(self):
        self.clear_content()
        animais_view.AnimaisView(self.content, self.animal_service)
    
    def show_habitats(self):
        self.clear_content()
        habitats_view.HabitatsView(self.content, self.habitat_service)
    
    def show_visitantes(self):
        self.clear_content()
        visitantes_view.VisitantesView(self.content, self.visita_service)
    
    def show_relatorios(self):
        self.clear_content()
        relatorios_view.RelatoriosView(self.content, self.zoo)
    
    def salvar_estado(self):
        try:
            self.zoo.salvar_estado('database/zoo_db.json')
            self.logger.log_info("Estado do zoológico salvo")
        except Exception as e:
            self.logger.log_erro(f"Erro ao salvar estado: {str(e)}")
    
    def sair(self):
        self.salvar_estado()
        self.root.quit()