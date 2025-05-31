from dataclasses import dataclass, field
from typing import List
from .animal import Animal

@dataclass
class Habitat:
    """Classe que representa um habitat no zoológico"""
    nome: str
    tipo: str  # Ex: "Savana", "Aquático", "Floresta"
    capacidade: int
    animais: List[Animal] = field(default_factory=list)
    
    def adicionar_animal(self, animal: Animal) -> bool:
        """Adiciona um animal ao habitat se houver capacidade"""
        if len(self.animais) < self.capacidade:
            self.animais.append(animal)
            return True
        return False
    
    def remover_animal(self, animal: Animal) -> bool:
        """Remove um animal do habitat"""
        if animal in self.animais:
            self.animais.remove(animal)
            return True
        return False
    
    def listar_animais(self) -> str:
        """Retorna string com lista de animais no habitat"""
        return ", ".join([animal.nome for animal in self.animais])
    
    def __str__(self) -> str:
        return (f"Habitat {self.nome} ({self.tipo}) - "
                f"{len(self.animais)}/{self.capacidade} animais")