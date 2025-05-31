import unittest
from package.models.animal import Mamifero, Ave, Reptil
from package.models.habitat import Habitat
from package.models.zoo import Zoo
from package.services.animal_service import AnimalService
from package.utils import Logger

class TestAnimais(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.zoo = Zoo("Zoológico Teste")
        self.habitat = Habitat("Savana", "Terrestre", 5)
        self.zoo.adicionar_habitat(self.habitat)
        self.service = AnimalService(self.zoo, self.logger)
    
    def test_cadastro_mamifero(self):
        dados = {
            'nome': 'Leão',
            'especie': 'Panthera leo',
            'idade': 5,
            'tipo': 'Mamifero',
            'pelagem': 'curta',
            'habitat': 'Savana'
        }
        resultado = self.service.cadastrar_animal(dados)
        self.assertTrue(resultado['sucesso'])
        self.assertEqual(len(self.zoo.animais), 1)
        self.assertIsInstance(self.zoo.animais[0], Mamifero)
    
    def test_cadastro_ave(self):
        dados = {
            'nome': 'Águia',
            'especie': 'Aquila chrysaetos',
            'idade': 3,
            'tipo': 'Ave',
            'envergadura': 2.5,
            'habitat': 'Savana'
        }
        resultado = self.service.cadastrar_animal(dados)
        self.assertTrue(resultado['sucesso'])
        self.assertEqual(self.zoo.animais[0].envergadura_asas, 2.5)
    
    def test_cadastro_reptil(self):
        dados = {
            'nome': 'Cobra',
            'especie': 'Python regius',
            'idade': 2,
            'tipo': 'Reptil',
            'escamas': 'escamosas',
            'habitat': 'Savana'
        }
        resultado = self.service.cadastrar_animal(dados)
        self.assertTrue(resultado['sucesso'])
        self.assertEqual(self.zoo.animais[0].escamas, 'escamosas')
    
    def test_cadastro_habitat_inexistente(self):
        dados = {
            'nome': 'Tigre',
            'especie': 'Panthera tigris',
            'idade': 4,
            'tipo': 'Mamifero',
            'pelagem': 'listrada',
            'habitat': 'Selva'  # Habitat não existe
        }
        resultado = self.service.cadastrar_animal(dados)
        self.assertFalse(resultado['sucesso'])
    
    def test_alimentar_animal(self):
        leao = Mamifero('Leão', 'Panthera leo', 5, 'curta')
        self.zoo.animais.append(leao)
        resultado = self.service.alimentar_animal('Leão')
        self.assertTrue(resultado['sucesso'])
        self.assertIn('foi alimentado', resultado['mensagem'])

if __name__ == '__main__':
    unittest.main()