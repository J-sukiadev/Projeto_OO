import tkinter as tk
from tkinter import ttk

def configure_styles(root):
    """Configura todos os estilos da aplicação"""
    style = ttk.Style(root)
    
    # Configurar tema base (pode ser 'clam', 'alt', 'default', 'classic')
    style.theme_use('clam')
    
    # ========== Configurações Gerais ==========
    style.configure('.', 
                  background='#f0f0f0', 
                  foreground='black',
                  font=('Arial', 10))
    
    style.configure('TFrame', background='#f0f0f0')
    style.configure('TLabel', background='#f0f0f0')
    style.configure('TButton', padding=6, relief='flat')
    style.configure('TEntry', fieldbackground='#ffffff')
    style.configure('TCombobox', fieldbackground='#ffffff')
    
    # ========== Estilos Personalizados ==========
    # Cabeçalhos
    style.configure('Header.TLabel', 
                  font=('Arial', 14, 'bold'),
                  foreground='#2c3e50')
    
    # Botões principais
    style.configure('Primary.TButton',
                  foreground='white',
                  background='#3498db',
                  font=('Arial', 10, 'bold'))
    style.map('Primary.TButton',
             background=[('active', '#2980b9')])
    
    # Botões de perigo (excluir, etc)
    style.configure('Danger.TButton',
                  foreground='white',
                  background='#e74c3c')
    style.map('Danger.TButton',
             background=[('active', '#c0392b')])
    
    # ========== Sidebar ==========
    style.configure('Sidebar.TFrame', 
                  background='#2c3e50')
    
    style.configure('Sidebar.TButton', 
                  foreground='white',
                  background='#34495e',
                  borderwidth=0,
                  font=('Arial', 11),
                  padding=10)
    style.map('Sidebar.TButton',
             background=[('active', '#2980b9')])
    
    # ========== Treeview (Tabelas) ==========
    style.configure('Treeview',
                  fieldbackground='#ffffff',
                  background='#ffffff',
                  foreground='black',
                  rowheight=25,
                  font=('Arial', 10))
    
    style.configure('Treeview.Heading',
                  background='#3498db',
                  foreground='white',
                  font=('Arial', 10, 'bold'),
                  padding=5)
    
    style.map('Treeview',
             background=[('selected', '#2980b9')],
             foreground=[('selected', 'white')])
    
    # ========== Notebook (Abas) ==========
    style.configure('TNotebook', background='#f0f0f0')
    style.configure('TNotebook.Tab',
                  padding=[10, 5],
                  background='#bdc3c7',
                  font=('Arial', 10))
    style.map('TNotebook.Tab',
             background=[('selected', '#3498db'), ('active', '#2980b9')],
             foreground=[('selected', 'white'), ('active', 'white')])