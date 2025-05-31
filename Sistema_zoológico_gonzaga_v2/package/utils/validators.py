import re
from typing import Union

class Validators:
    """
    Classe com métodos estáticos para validação de dados.
    """
    
    @staticmethod
    def validar_cpf(cpf: str) -> bool:
        """
        Validação de CPF (formato e dígitos verificadores).
        
        Args:
            cpf: String com o CPF a ser validado
            
        Returns:
            True se o CPF for válido
        """
        cpf = ''.join(filter(str.isdigit, cpf))
        
        if len(cpf) != 11 or cpf == cpf[0] * 11:
            return False
            
        # Cálculo do primeiro dígito verificador
        soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
        resto = 11 - (soma % 11)
        digito1 = resto if resto < 10 else 0
        
        # Cálculo do segundo dígito verificador
        soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
        resto = 11 - (soma % 11)
        digito2 = resto if resto < 10 else 0
        
        return int(cpf[9]) == digito1 and int(cpf[10]) == digito2
    
    @staticmethod
    def validar_idade(idade: Union[str, int]) -> bool:
        """
        Valida se a idade está em um intervalo razoável (1-120 anos).
        
        Args:
            idade: Idade como string ou inteiro
            
        Returns:
            True se a idade for válida
        """
        try:
            idade_int = int(idade)
            return 1 <= idade_int <= 120
        except (ValueError, TypeError):
            return False
    
    @staticmethod
    def validar_nome(nome: str) -> bool:
        """
        Validação básica de nome (mais que 2 caracteres, sem números).
        
        Args:
            nome: String a ser validada
            
        Returns:
            True se o nome for válido
        """
        nome = nome.strip()
        return (
            len(nome) > 2 and 
            '  ' not in nome and
            all(c.isalpha() or c.isspace() or c in "-'." for c in nome)
        )
    
    @staticmethod
    def validar_capacidade(capacidade: Union[str, int]) -> bool:
        """
        Valida a capacidade de habitats (1-1000 animais).
        
        Args:
            capacidade: Capacidade como string ou inteiro
            
        Returns:
            True se a capacidade for válida
        """
        try:
            cap = int(capacidade)
            return 1 <= cap <= 1000
        except (ValueError, TypeError):
            return False
    
    @staticmethod
    def validar_telefone(telefone: str) -> bool:
        """
        Validação básica de telefone (formato brasileiro).
        
        Args:
            telefone: String com o telefone
            
        Returns:
            True se o formato for válido
        """
        telefone = ''.join(filter(str.isdigit, telefone))
        return 10 <= len(telefone) <= 11
    
    @staticmethod
    def validar_data(data_str: str, formato: str = '%d/%m/%Y') -> bool:
        """
        Valida se uma string representa uma data válida.
        
        Args:
            data_str: String com a data
            formato: Formato esperado (padrão dd/mm/aaaa)
            
        Returns:
            True se a data for válida
        """
        try:
            from datetime import datetime
            datetime.strptime(data_str, formato)
            return True
        except ValueError:
            return False