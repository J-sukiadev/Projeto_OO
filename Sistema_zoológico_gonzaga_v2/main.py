import tkinter as tk
from tkinter import ttk, messagebox
from package.models.zoo import Zoo
from package.utils import Logger
from views.menu_principal import MenuPrincipal
import os
import json

class Aplicacao:
    def __init__(self, root):
        """Classe principal da aplicação que gerencia todo o sistema"""
        self.root = root  # Janela principal 
        self.configurar_interface()  # Configura aparência inicial
        self.inicializar_componentes()  # Inicializa serviços e dados
        self.iniciar_aplicacao()  # Inicia a interface principal

    def configurar_interface(self):
        """Configura propriedades básicas da janela principal"""
        self.root.title("ZooSys - Sistema de Gerenciamento de Zoológico")
        self.root.geometry("1200x700")  # Tamanho inicial
        self.root.minsize(1000, 600)  # Tamanho mínimo
        self.configurar_estilos()  # Aplica estilos visuais

    def configurar_estilos(self):
        """Define os estilos visuais para os componentes da interface"""
        style = ttk.Style(self.root)
        style.theme_use('clam')  
        
        # Estilos base para todos os componentes
        style.configure('.', background='#f0f0f0')  # Cor de fundo geral
        style.configure('TFrame', background='#f0f0f0')  # Frames
        style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))  # Labels
        style.configure('TButton', font=('Arial', 10), padding=5)  # Botões
        
        # Estilos personalizados para componentes específicos:
        style.configure('Header.TLabel', font=('Arial', 14, 'bold'))  # Cabeçalhos
        style.configure('Sidebar.TFrame', background='#2c3e50')  # Barra lateral
        style.configure('Sidebar.TButton', 
                      foreground='white', 
                      background='#34495e', 
                      borderwidth=0, 
                      font=('Arial', 11))  # Botões da sidebar
        
        # Efeito hover para botões da sidebar
        style.map('Sidebar.TButton', background=[('active', "#c063dc")])

    def verificar_banco_dados(self):
        """
        Verifica e inicializa o arquivo JSON de banco de dados
        Retorna True se o arquivo já existia, False se foi criado novo
        """
        db_path = 'database/zoo_db.json'
        os.makedirs(os.path.dirname(db_path), exist_ok=True)  # Cria pasta se não existir
        
        if not os.path.exists(db_path):
            # Cria estrutura inicial do JSON se o arquivo não existir
            with open(db_path, 'w', encoding='utf-8') as f:
                json.dump({
                    "nome": "Zoológico Virtual",
                    "habitats": [],
                    "animais": [],
                    "visitantes": [],
                    "ingressos": []
                }, f, indent=2)
            return False
        return True

    def inicializar_componentes(self):
        """Inicializa os principais componentes da aplicação"""
        self.logger = Logger()  # Sistema de log
        self.zoo = Zoo("Zoológico Virtual")  # Modelo principal
        
        # Tenta carregar dados existentes
        if self.verificar_banco_dados():
            try:
                if not self.zoo.carregar_estado('database/zoo_db.json'):
                    self.logger.log_info("Banco de dados vazio ou inválido. Iniciando novo.")
            except Exception as e:
                self.logger.log_erro(f"Erro ao carregar dados: {str(e)}")
                # Mostra erro ao usuário mas permite continuar
                messagebox.showerror("Erro", "Falha ao carregar dados existentes.")

    def iniciar_aplicacao(self):
        """Inicia a interface principal do sistema"""
        self.menu_principal = MenuPrincipal(self.root, self.zoo, self.logger)
        self.configurar_fechamento()  # Configura comportamento ao fechar
        self.centralizar_janela()  # Centraliza na tela

    def configurar_fechamento(self):
        """Configura o comportamento seguro ao fechar a aplicação"""
        def on_closing():
            # Diálogo de confirmação
            if messagebox.askokcancel("Sair", "Deseja realmente sair? Todos os dados serão salvos."):
                try:
                    # Salva o estado atual antes de sair
                    self.zoo.salvar_estado('database/zoo_db.json')
                    self.logger.log_info("Aplicação encerrada com sucesso")
                except Exception as e:
                    self.logger.log_erro(f"Erro ao salvar ao sair: {str(e)}")
                finally:
                    self.root.destroy()  # Fecha a aplicação
        
        # Vincula a função ao evento de fechamento da janela
        self.root.protocol("WM_DELETE_WINDOW", on_closing)

    def centralizar_janela(self):
        """Centraliza a janela principal na tela do usuário"""
        self.root.update_idletasks()  # Atualiza geometria
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        # Calcula posição central
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

def main():
    """Função principal de entrada da aplicação"""
    root = tk.Tk()  # Cria a instância principal do Tkinter
    app = Aplicacao(root)  # Inicia a aplicação
    
    try:
        root.mainloop()  # Inicia o loop principal de eventos
    except Exception as e:
        # Captura erros não tratados no loop principal
        Logger().log_erro(f"Erro fatal: {str(e)}")
        raise  # Re-lança a exceção para depuração

if __name__ == "__main__":
    # Ponto de entrada quando executado diretamente
    main()