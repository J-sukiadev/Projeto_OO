import unittest
import os
import json
from tempfile import mkstemp
from package.models.zoo import Zoo
from package.models.animal import Mamifero
from package.models.habitat import Habitat
from package.models.visitante import Visitante

class TestZoo(unittest.TestCase):
    def setUp(self):
        self.zoo = Zoo("Zoológico Teste")
        self.habitat = Habitat("Savana", "Terrestre", 5)
        self.zoo.adicionar_habitat(self.habitat)
        self.animal = Mamifero("Leão", "Panthera leo", 5, "curta")
        self.zoo.adicionar_animal(self.animal, "Savana")
        self.visitante = Visitante("João Silva", 30, "VIS123")
        self.zoo.registrar_visita(self.visitante)
    
    def test_salvar_estado(self):
        fd, path = mkstemp(suffix='.json')
        try:
            self.zoo.salvar_estado(path)
            with open(path, 'r') as f:
                data = json.load(f)
                self.assertEqual(data['nome'], "Zoológico Teste")
                self.assertEqual(len(data['habitats']), 1)
        finally:
            os.remove(path)
    
    def test_carregar_estado(self):
        fd, path = mkstemp(suffix='.json')
        try:
            # Salva estado inicial
            self.zoo.salvar_estado(path)
            
            # Cria novo zoo e carrega
            novo_zoo = Zoo("Novo Zoo")
            resultado = novo_zoo.carregar_estado(path)
            
            self.assertTrue(resultado)
            self.assertEqual(novo_zoo.nome, "Zoológico Teste")
            self.assertEqual(len(novo_zoo.habitats), 1)
        finally:
            os.remove(path)
    
    def test_carregar_arquivo_inexistente(self):
        resultado = self.zoo.carregar_estado("arquivo_inexistente.json")
        self.assertFalse(resultado)

if __name__ == '__main__':
    unittest.main()