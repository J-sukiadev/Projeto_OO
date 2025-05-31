from typing import List, Dict
from package.models.habitat import Habitat
from package.utils import Logger, Validators

class HabitatService:
    def __init__(self, zoo, logger: Logger):
        self.zoo = zoo
        self.logger = logger
    
    def criar_habitat(self, dados: Dict) -> Dict:
        """Cria um novo habitat com validações"""
        try:
            # Validações
            if not Validators.validar_nome(dados.get('nome', '')):
                return {'sucesso': False, 'mensagem': 'Nome do habitat inválido'}
            
            capacidade = dados.get('capacidade', '0')
            if not capacidade.isdigit() or not Validators.validar_capacidade(int(capacidade)):
                return {'sucesso': False, 'mensagem': 'Capacidade deve ser entre 1 e 100'}
            
            # Criação do habitat
            habitat = Habitat(
                nome=dados['nome'],
                tipo=dados['tipo'],
                capacidade=int(capacidade)
            )
            
            self.zoo.adicionar_habitat(habitat)
            self.logger.log_info(f"Habitat criado: {habitat.nome}", {
                'tipo': habitat.tipo,
                'capacidade': habitat.capacidade
            })
            self.zoo.salvar_estado('database/zoo_db.json')
            return {'sucesso': True, 'habitat': habitat}
            
        except Exception as e:
            self.logger.log_erro("Erro ao criar habitat", e)
            return {'sucesso': False, 'mensagem': str(e)}
    
    def listar_habitats(self) -> List[Dict]:
        """Retorna lista de habitats formatada para a view"""
        try:
            habitats = []
            for habitat in self.zoo.habitats:
                habitats.append({
                    'nome': habitat.nome,
                    'tipo': habitat.tipo,
                    'capacidade': habitat.capacidade,
                    'animais': [a.nome for a in habitat.animais],
                    'vagas': habitat.capacidade - len(habitat.animais)
                })
            
            self.logger.log_info("Listagem de habitats realizada")
            return habitats
            
        except Exception as e:
            self.logger.log_erro("Erro ao listar habitats", e)
            return []
    
    def remover_habitat(self, nome_habitat: str) -> Dict:
        """Remove um habitat do sistema"""
        try:
            for habitat in self.zoo.habitats[:]:
                if habitat.nome == nome_habitat:
                    if habitat.animais:
                        return {
                            'sucesso': False,
                            'mensagem': 'Não é possível remover habitat com animais'
                        }
                    
                    self.zoo.habitats.remove(habitat)
                    self.logger.log_info(f"Habitat removido: {nome_habitat}")
                    self.zoo.salvar_estado('database/zoo_db.json')
                    return {'sucesso': True}
            
            return {'sucesso': False, 'mensagem': 'Habitat não encontrado'}
        except Exception as e:
            self.logger.log_erro(f"Erro ao remover habitat {nome_habitat}", e)
            return {'sucesso': False, 'mensagem': str(e)}
    
    def exportar_para_json(self, arquivo: str) -> Dict:
        """Exporta habitats para arquivo JSON"""
        try:
            dados = [{
                'nome': h.nome,
                'tipo': h.tipo,
                'capacidade': h.capacidade,
                'animais': [a.nome for a in h.animais]
            } for h in self.zoo.habitats]
            
            import os
            os.makedirs(os.path.dirname(arquivo), exist_ok=True)
            
            with open(arquivo, 'w', encoding='utf-8') as f:
                import json
                json.dump(dados, f, indent=2, ensure_ascii=False)
            
            self.logger.log_info(f"Habitats exportados para {arquivo}")
            return {'sucesso': True, 'arquivo': arquivo}
            
        except Exception as e:
            self.logger.log_erro(f"Erro ao exportar habitats para {arquivo}", e)
            return {'sucesso': False, 'mensagem': str(e)}