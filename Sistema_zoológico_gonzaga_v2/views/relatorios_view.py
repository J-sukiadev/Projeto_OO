import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from package.models.animal import Mamifero, Ave, Reptil

class RelatoriosView:
    def __init__(self, parent, zoo):
        self.parent = parent
        self.zoo = zoo
        self.setup_ui()
    
    def setup_ui(self):
        # Frame de cabeçalho
        header_frame = ttk.Frame(self.parent)
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(header_frame, text="Relatórios", style='Header.TLabel').pack(side=tk.LEFT)
        
        # Frame de seleção
        selection_frame = ttk.Frame(self.parent)
        selection_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(selection_frame, text="Tipo de relatório:").pack(side=tk.LEFT)
        
        self.report_type = tk.StringVar()
        report_options = ['Animais', 'Habitats', 'Visitantes', 'Financeiro']
        report_dropdown = ttk.Combobox(
            selection_frame,
            textvariable=self.report_type,
            values=report_options,
            state='readonly'
        )
        report_dropdown.pack(side=tk.LEFT, padx=5)
        report_dropdown.current(0)
        
        ttk.Button(selection_frame, text="Gerar", command=self.gerar_relatorio).pack(side=tk.LEFT, padx=5)
        ttk.Button(selection_frame, text="Exportar", command=self.exportar_relatorio).pack(side=tk.LEFT, padx=5)
        
        # Área de texto para o relatório
        self.report_text = tk.Text(
            self.parent,
            wrap=tk.WORD,
            font=('Consolas', 10),
            padx=10,
            pady=10
        )
        scrollbar = ttk.Scrollbar(self.parent, command=self.report_text.yview)
        self.report_text.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.report_text.pack(fill=tk.BOTH, expand=True)
        
        # Gerar relatório inicial
        self.gerar_relatorio()
    
    def gerar_relatorio(self):
        tipo = self.report_type.get()
        relatorio = ""
        
        if tipo == "Animais":
            relatorio = self._relatorio_animais()
        elif tipo == "Habitats":
            relatorio = self._relatorio_habitats()
        elif tipo == "Visitantes":
            relatorio = self._relatorio_visitantes()
        else:
            relatorio = self._relatorio_financeiro()
        
        self.report_text.delete(1.0, tk.END)
        self.report_text.insert(tk.END, relatorio)
    
    def _relatorio_animais(self):
        total = len(self.zoo.animais)
        mamiferos = sum(1 for a in self.zoo.animais if isinstance(a, Mamifero))
        aves = sum(1 for a in self.zoo.animais if isinstance(a, Ave))
        repteis = total - mamiferos - aves
        
        return (
            f"RELATÓRIO DE ANIMAIS\n"
            f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n"
            f"Total de animais: {total}\n"
            f"Mamíferos: {mamiferos}\n"
            f"Aves: {aves}\n"
            f"Répteis: {repteis}\n\n"
            f"Lista completa:\n"
            + "\n".join(f"- {a.nome} ({a.especie}), {a.idade} anos" 
                       for a in self.zoo.animais)
        )
    
    def _relatorio_habitats(self):
        return (
            f"RELATÓRIO DE HABITATS\n"
            f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n"
            f"Total de habitats: {len(self.zoo.habitats)}\n"
            f"Capacidade total: {sum(h.capacidade for h in self.zoo.habitats)}\n"
            f"Animais alojados: {sum(len(h.animais) for h in self.zoo.habitats)}\n\n"
            + "\n".join(
                f"{h.nome} ({h.tipo}): {len(h.animais)}/{h.capacidade} animais\n"
                f"  Animais: {', '.join(a.nome for a in h.animais) or 'Nenhum'}"
                for h in self.zoo.habitats
            )
        )
    
    def _relatorio_visitantes(self):
        total = len(self.zoo.visitantes)
        criancas = sum(1 for v in self.zoo.visitantes if v.idade < 12)
        idosos = sum(1 for v in self.zoo.visitantes if v.idade >= 60)
        
        return (
            f"RELATÓRIO DE VISITANTES\n"
            f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n"
            f"Total de visitantes: {total}\n"
            f"Crianças (<12 anos): {criancas}\n"
            f"Adultos: {total - criancas - idosos}\n"
            f"Idosos (≥60 anos): {idosos}\n\n"
            f"Ingressos vendidos: {len(self.zoo.ingressos)}\n"
        )
    
    def _relatorio_financeiro(self):
        total_ingressos = sum(i.valor for i in self.zoo.ingressos)
        visitantes = len(self.zoo.visitantes)
        
        return (
            f"RELATÓRIO FINANCEIRO\n"
            f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n"
            f"Receita total: R$ {total_ingressos:.2f}\n"
            f"Média por visitante: R$ {total_ingressos/visitantes:.2f}\n" if visitantes > 0 else ""
            f"Visitantes atendidos: {visitantes}\n"
        )
    
    def exportar_relatorio(self):
        # Implementação básica - poderia salvar em arquivo .txt
        messagebox.showinfo("Info", "Funcionalidade de exportação será implementada")