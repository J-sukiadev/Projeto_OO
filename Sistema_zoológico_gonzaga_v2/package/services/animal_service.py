from typing import List, Dict, Optional
from package.models.animal import Animal, Mamifero, Ave, Reptil
from package.models.habitat import Habitat
from package.utils import Logger, Validators

class AnimalService:
    def __init__(self, zoo, logger: Logger):
        self.zoo = zoo
        self.logger = logger
    
    def cadastrar_animal(self, dados: Dict) -> Dict:
        """Cadastra um novo animal com validações e logging"""
        try:
            # Validação básica
            if not Validators.validar_nome(dados.get('nome', '')):
                return {'sucesso': False, 'mensagem': 'Nome do animal inválido'}
            
            idade = dados.get('idade', '0')
            if not idade.isdigit() or not Validators.validar_idade(int(idade)):
                return {'sucesso': False, 'mensagem': 'Idade do animal inválida'}
            
            # Criação do animal conforme tipo
            tipo = dados['tipo']
            if tipo == 'Mamifero':
                animal = Mamifero(
                    nome=dados['nome'],
                    especie=dados['especie'],
                    idade=int(idade),
                    pelagem=dados.get('pelagem', 'curta')
                )
            elif tipo == 'Ave':
                animal = Ave(
                    nome=dados['nome'],
                    especie=dados['especie'],
                    idade=int(idade),
                    envergadura_asas=float(dados.get('envergadura', 1.0))
                )
            else:  # Réptil
                animal = Reptil(
                    nome=dados['nome'],
                    especie=dados['especie'],
                    idade=int(idade),
                    escamas=dados.get('escamas', 'escamosas')
                )
            
            # Adiciona ao habitat
            sucesso = self.zoo.adicionar_animal(animal, dados['habitat'])
            
            if sucesso:
                self.logger.log_info(f"Animal cadastrado: {animal.nome}", {
                    'tipo': tipo,
                    'habitat': dados['habitat']
                })
                self.zoo.salvar_estado('database/zoo_db.json')
                return {'sucesso': True, 'animal': animal}
            
            return {'sucesso': False, 'mensagem': 'Habitat sem capacidade ou não encontrado'}
            
        except Exception as e:
            self.logger.log_erro("Erro ao cadastrar animal", e)
            return {'sucesso': False, 'mensagem': str(e)}
    
    def editar_animal(self, nome_original: str, novos_dados: Dict) -> Dict:
        """Edita um animal existente no sistema"""
        try:
            # Validações
            if not Validators.validar_nome(novos_dados.get('nome', '')):
                return {'sucesso': False, 'mensagem': 'Nome do animal inválido'}
            
            idade = novos_dados.get('idade', '0')
            if not idade.isdigit() or not Validators.validar_idade(int(idade)):
                return {'sucesso': False, 'mensagem': 'Idade do animal inválida'}
            
            # Encontra o animal a ser editado
            animal_original = None
            for animal in self.zoo.animais:
                if animal.nome == nome_original:
                    animal_original = animal
                    break
            
            if not animal_original:
                return {'sucesso': False, 'mensagem': 'Animal não encontrado'}
            
            # Remove o animal original (será recriado)
            self.zoo.animais.remove(animal_original)
            for habitat in self.zoo.habitats:
                if animal_original in habitat.animais:
                    habitat.animais.remove(animal_original)
            
            # Cria o animal atualizado
            tipo = novos_dados['tipo']
            if tipo == 'Mamifero':
                animal = Mamifero(
                    nome=novos_dados['nome'],
                    especie=novos_dados['especie'],
                    idade=int(idade),
                    pelagem=novos_dados.get('pelagem', 'curta')
                )
            elif tipo == 'Ave':
                animal = Ave(
                    nome=novos_dados['nome'],
                    especie=novos_dados['especie'],
                    idade=int(idade),
                    envergadura_asas=float(novos_dados.get('envergadura', 1.0))
                )
            else:  # Réptil
                animal = Reptil(
                    nome=novos_dados['nome'],
                    especie=novos_dados['especie'],
                    idade=int(idade),
                    escamas=novos_dados.get('escamas', 'escamosas')
                )
            
            # Adiciona ao novo habitat
            sucesso = self.zoo.adicionar_animal(animal, novos_dados['habitat'])
            
            if sucesso:
                self.logger.log_info(f"Animal editado: {nome_original} -> {animal.nome}")
                self.zoo.salvar_estado('database/zoo_db.json')
                return {'sucesso': True, 'animal': animal}
            
            return {'sucesso': False, 'mensagem': 'Falha ao atualizar habitat do animal'}
            
        except Exception as e:
            self.logger.log_erro(f"Erro ao editar animal {nome_original}", e)
            return {'sucesso': False, 'mensagem': str(e)}
    
    def obter_detalhes_animal(self, nome_animal: str) -> Optional[Dict]:
        """Obtém detalhes específicos de um animal"""
        for animal in self.zoo.animais:
            if animal.nome == nome_animal:
                detalhes = {
                    'nome': animal.nome,
                    'especie': animal.especie,
                    'idade': animal.idade,
                    'tipo': animal.__class__.__name__,
                    'habitat': self._encontrar_habitat_animal(animal)
                }
                
                # Adiciona campos específicos
                if isinstance(animal, Mamifero):
                    detalhes['pelagem'] = animal.pelagem
                elif isinstance(animal, Ave):
                    detalhes['envergadura'] = animal.envergadura_asas
                elif isinstance(animal, Reptil):
                    detalhes['escamas'] = animal.escamas
                
                return detalhes
        return None
    
    def listar_animais(self) -> List[Dict]:
        """Retorna lista de animais formatada para a view"""
        try:
            animais = []
            for animal in self.zoo.animais:
                habitat = self._encontrar_habitat_animal(animal)
                animais.append({
                    'nome': animal.nome,
                    'especie': animal.especie,
                    'idade': animal.idade,
                    'tipo': animal.__class__.__name__,
                    'habitat': habitat
                })
        
            self.logger.log_info("Listagem de animais realizada")
            return animais
        
        except Exception as e:
            self.logger.log_erro(f"Erro ao listar animais: {str(e)}")
            return []
    
    def remover_animal(self, nome_animal: str) -> Dict:
        """Remove um animal do sistema"""
        try:
            for animal in self.zoo.animais[:]:
                if animal.nome == nome_animal:
                    # Remove do habitat primeiro
                    for habitat in self.zoo.habitats:
                        if animal in habitat.animais:
                            habitat.animais.remove(animal)
                    
                    # Remove da lista principal
                    self.zoo.animais.remove(animal)
                    self.logger.log_info(f"Animal removido: {nome_animal}")
                    self.zoo.salvar_estado('database/zoo_db.json')
                    return {'sucesso': True, 'mensagem': 'Animal removido com sucesso'}
            
            return {'sucesso': False, 'mensagem': 'Animal não encontrado'}
        except Exception as e:
            self.logger.log_erro(f"Erro ao remover animal {nome_animal}", e)
            return {'sucesso': False, 'mensagem': str(e)}
    
    def _encontrar_habitat_animal(self, animal: Animal) -> Optional[str]:
        """Método auxiliar para encontrar habitat de um animal"""
        for habitat in self.zoo.habitats:
            if animal in habitat.animais:
                return habitat.nome
        return None