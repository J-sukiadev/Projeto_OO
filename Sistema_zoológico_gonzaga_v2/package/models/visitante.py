from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Visitante:
    """Classe que representa um visitante do zoológico"""
    nome: str
    idade: int
    id_visitante: str = ""
    
    def __post_init__(self):
        """Gera ID automático se não fornecido"""
        if not self.id_visitante:
            self.id_visitante = f"VIS{hash((self.nome, self.idade)) % 10000:04d}"
    
    def __str__(self) -> str:
        return f"Visitante: {self.nome} (ID: {self.id_visitante})"

@dataclass
class Ingresso:
    """Classe que representa um ingresso vendido"""
    visitante: Visitante
    data: datetime
    valor: float = 50.0
    codigo: str = ""
    
    def __post_init__(self):
        """Gera código do ingresso e calcula desconto"""
        self.codigo = f"ING{hash((self.visitante.id_visitante, self.data)) % 10000:04d}"
        self.calcular_desconto()
    
    def calcular_desconto(self) -> None:
        """Aplica desconto para crianças e idosos"""
        if self.visitante.idade < 12 or self.visitante.idade >= 60:
            self.valor *= 0.5  # 50% de desconto
    
    def __str__(self) -> str:
        return (f"Ingresso {self.codigo} - {self.visitante.nome} - "
                f"R${self.valor:.2f} - {self.data.strftime('%d/%m/%Y')}")