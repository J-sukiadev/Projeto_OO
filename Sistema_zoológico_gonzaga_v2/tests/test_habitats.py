import unittest
from package.models.habitat import Habitat
from package.models.zoo import Zoo
from package.services.habitat_service import HabitatService
from package.utils import Logger

class TestHabitats(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.zoo = Zoo("Zoológico Teste")
        self.service = HabitatService(self.zoo, self.logger)
    
    def test_criar_habitat(self):
        dados = {
            'nome': 'Aquário',
            'tipo': 'Aquático',
            'capacidade': '10'
        }
        resultado = self.service.criar_habitat(dados)
        self.assertTrue(resultado['sucesso'])
        self.assertEqual(len(self.zoo.habitats), 1)
        self.assertEqual(self.zoo.habitats[0].nome, 'Aquário')
    
    def test_capacidade_invalida(self):
        dados = {
            'nome': 'Savana',
            'tipo': 'Terrestre',
            'capacidade': '0'  # Capacidade inválida
        }
        resultado = self.service.criar_habitat(dados)
        self.assertFalse(resultado['sucesso'])
        self.assertEqual(len(self.zoo.habitats), 0)
    
    def test_listar_habitats(self):
        self.zoo.adicionar_habitat(Habitat("Savana", "Terrestre", 5))
        habitats = self.service.listar_habitats()
        self.assertEqual(len(habitats), 1)
        self.assertEqual(habitats[0]['nome'], 'Savana')

if __name__ == '__main__':
    unittest.main()