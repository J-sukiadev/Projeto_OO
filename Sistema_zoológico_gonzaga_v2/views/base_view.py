# views/base_view.py
import tkinter as tk
from tkinter import ttk, messagebox

class BaseView:
    def __init__(self, parent):
        self.parent = parent
        self.setup_ui()
    
    def setup_ui(self):
        pass
        
    def show_error(self, message):
        messagebox.showerror("Erro", message)
        
    def show_info(self, message):
        messagebox.showinfo("Informação", message)