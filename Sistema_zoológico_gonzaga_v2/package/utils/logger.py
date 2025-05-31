import logging
from datetime import datetime
from typing import Any, Optional

class Logger:
    """
    Classe para gerenciamento de logs do sistema com múltiplos níveis e formatação consistente.
    Implementa o padrão Singleton para garantir uma única instância global.
    """
    
    _instance = None
    
    def __new__(cls, nome_arquivo: str = 'zoosys.log'):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.__inicializado = False
        return cls._instance
    
    def __init__(self, nome_arquivo: str = 'zoosys.log'):
        if not self.__inicializado:
            self.nome_arquivo = nome_arquivo
            self._configurar_logger()
            self.__inicializado = True
    
    def _configurar_logger(self):
        """Configura o sistema de logging com formatação e handlers."""
        self.logger = logging.getLogger('ZooSys')
        self.logger.setLevel(logging.INFO)
        
        # Formatação padrão
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%d/%m/%Y %H:%M:%S'
        )
        
        # Handler para arquivo
        file_handler = logging.FileHandler(self.nome_arquivo)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        
        # Handler para console (apenas durante desenvolvimento)
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
    
    def log_info(self, mensagem: str, dados: Optional[Any] = None):
        """
        Registra uma mensagem informativa no log.
        
        Args:
            mensagem (str): Mensagem principal
            dados (Any, optional): Dados adicionais para registro
        """
        if dados:
            mensagem += f" | Dados: {str(dados)}"
        self.logger.info(mensagem)
    
    def log_erro(self, mensagem: str, excecao: Optional[Exception] = None):
        """
        Registra uma mensagem de erro no log.
        
        Args:
            mensagem (str): Descrição do erro
            excecao (Exception, optional): Exceção relacionada
        """
        if excecao:
            mensagem += f" | Exceção: {str(excecao)}"
        self.logger.error(mensagem)
    
    def log_debug(self, mensagem: str, variaveis: Optional[dict] = None):
        """
        Registra mensagem de debug (ativo apenas em modo desenvolvimento).
        
        Args:
            mensagem (str): Mensagem de debug
            variaveis (dict, optional): Variáveis relevantes
        """
        if variaveis:
            mensagem += f" | Variáveis: {str(variaveis)}"
        self.logger.debug(mensagem)
    
    @staticmethod
    def log_rapido(mensagem: str):
        """
        Método estático para logs rápidos no console.
        Não grava no arquivo de log.
        
        Args:
            mensagem (str): Mensagem a ser exibida
        """
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {mensagem}")

    def __repr__(self):
        return f"Logger(arquivo='{self.nome_arquivo}')"