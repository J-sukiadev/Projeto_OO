from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class Animal(ABC):
    nome: str
    especie: str
    idade: int
    
    @abstractmethod
    def fazer_barulho(self):
        pass

@dataclass
class Mamifero(Animal):
    pelagem: str
    
    def fazer_barulho(self):
        return f"{self.nome} está fazendo barulho!"

@dataclass
class Ave(Animal):
    envergadura_asas: float
    
    def fazer_barulho(self):
        return f"{self.nome} está fazendo barulho!"

@dataclass
class Reptil(Animal):
    escamas: str
    
    def fazer_barulho(self):
        return f"{self.nome} está fazendo barulho!"
    #talvez usar função de barulhos, talvez não ¯\_(ツ)_/¯