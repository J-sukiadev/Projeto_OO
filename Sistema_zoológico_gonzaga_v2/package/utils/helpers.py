import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from datetime import datetime

class Helpers:
    """
    Classe utilitária com métodos estáticos para operações comuns.
    """
    
    @staticmethod
    def carregar_json(arquivo: Union[str, Path]) -> Dict[str, Any]:
        """
        Carrega dados de um arquivo JSON com tratamento de erros robusto.
        
        Args:
            arquivo: Caminho para o arquivo JSON
            
        Returns:
            Dicionário com os dados carregados ou vazio se falhar
            
        Raises:
            TypeError: Se o caminho não for str ou Path
        """
        if not isinstance(arquivo, (str, Path)):
            raise TypeError("O caminho deve ser str ou Path")
        
        try:
            path = Path(arquivo)
            if path.exists() and path.stat().st_size > 0:
                with open(path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {}
        except json.JSONDecodeError:
            Helpers.log_rapido(f"Arquivo JSON inválido: {arquivo}")
            return {}
        except Exception as e:
            Helpers.log_rapido(f"Erro ao carregar JSON: {e}")
            return {}
    
    @staticmethod
    def salvar_json(arquivo: Union[str, Path], dados: Dict[str, Any]) -> bool:
        """
        Salva dados em um arquivo JSON com formatação e criação de diretórios.
        
        Args:
            arquivo: Caminho para o arquivo de saída
            dados: Dicionário com dados a serem salvos
            
        Returns:
            True se bem-sucedido, False caso contrário
        """
        try:
            path = Path(arquivo)
            path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(dados, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            Helpers.log_rapido(f"Erro ao salvar JSON: {e}")
            return False
    
    @staticmethod
    def formatar_data(data: datetime) -> str:
        """
        Formata um objeto datetime para string legível.
        
        Args:
            data: Objeto datetime a ser formatado
            
        Returns:
            String no formato 'dd/mm/aaaa HH:MM'
        """
        return data.strftime("%d/%m/%Y %H:%M")
    
    @staticmethod
    def listar_para_combo(dados: List[Any], campo: str = 'nome') -> List[Dict[str, Any]]:
        """
        Prepara uma lista de objetos para uso em combobox.
        
        Args:
            dados: Lista de objetos
            campo: Nome do atributo a ser exibido
            
        Returns:
            Lista de dicionários no formato {'nome': valor, 'objeto': obj}
        """
        return [{'nome': getattr(item, campo), 'objeto': item} for item in dados]
    
    @staticmethod
    def validar_email(email: str) -> bool:
        """
        Validação básica de formato de e-mail.
        
        Args:
            email: String a ser validada
            
        Returns:
            True se o formato for válido
        """
        return '@' in email and '.' in email.split('@')[-1]
    
    @staticmethod
    def log_rapido(mensagem: str):
        """
        Atalho para log rápido no console (usado antes do Logger estar disponível).
        """
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {mensagem}")

    @staticmethod
    def criar_backup(arquivo: Union[str, Path]) -> bool:
        """
        Cria um backup do arquivo com timestamp.
        
        Args:
            arquivo: Caminho do arquivo original
            
        Returns:
            True se o backup for bem-sucedido
        """
        try:
            path = Path(arquivo)
            if not path.exists():
                return False
                
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = path.with_name(f"{path.stem}_backup_{timestamp}{path.suffix}")
            
            import shutil
            shutil.copy2(path, backup_path)
            return True
        except Exception as e:
            Helpers.log_rapido(f"Erro ao criar backup: {e}")
            return False