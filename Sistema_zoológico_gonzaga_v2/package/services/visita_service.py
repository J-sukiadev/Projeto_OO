from datetime import datetime
from typing import List, Dict
from package.models.visitante import Visitante, Ingresso
from package.utils import Logger, Validators, Helpers

class VisitaService:
    def __init__(self, zoo, logger: Logger):
        self.zoo = zoo
        self.logger = logger
    
    def registrar_visita(self, dados: Dict) -> Dict:
        """Registra uma nova visita com validações"""
        try:
            # Validações
            if not Validators.validar_nome(dados.get('nome', '')):
                return {'sucesso': False, 'mensagem': 'Nome do visitante inválido'}
            
            idade = dados.get('idade', '0')
            if not idade.isdigit() or not Validators.validar_idade(int(idade)):
                return {'sucesso': False, 'mensagem': 'Idade do visitante inválida'}
            
            # Registro da visita
            visitante = Visitante(
                nome=dados['nome'],
                idade=int(idade),
                id_visitante=dados.get('id', '')
            )
            
            ingresso = self.zoo.registrar_visita(visitante)
            
            self.logger.log_info(f"Visita registrada: {visitante.nome}", {
                'ingresso': ingresso.codigo,
                'valor': ingresso.valor
            })
            self.zoo.salvar_estado('database/zoo_db.json')
            
            return {
                'sucesso': True,
                'visitante': visitante,
                'ingresso': {
                    'codigo': ingresso.codigo,
                    'valor': ingresso.valor,
                    'data': Helpers.formatar_data(ingresso.data)
                }
            }
            
        except Exception as e:
            self.logger.log_erro("Erro ao registrar visita", e)
            return {'sucesso': False, 'mensagem': str(e)}
    
    def listar_visitantes(self) -> List[Dict]:
        """Retorna lista de visitantes formatada para a view"""
        try:
            visitantes = []
            for visitante in self.zoo.visitantes:
                visitantes.append({
                    'nome': visitante.nome,
                    'idade': visitante.idade,
                    'ingressos': self._contar_visitas(visitante)
                })
            
            self.logger.log_info("Listagem de visitantes realizada")
            return visitantes
            
        except Exception as e:
            self.logger.log_erro("Erro ao listar visitantes", e)
            return []
    
    def _contar_visitas(self, visitante: Visitante) -> int:
        """Conta visitas de um visitante"""
        return sum(1 for i in self.zoo.ingressos if i.visitante == visitante)
    
    def gerar_relatorio_visitantes(self) -> Dict:
        """Gera relatório completo de visitantes"""
        try:
            estatisticas = self._calcular_estatisticas()
            visitantes = self.listar_visitantes()
            
            relatorio = {
                'estatisticas': estatisticas,
                'visitantes': visitantes,
                'data_geracao': Helpers.formatar_data(datetime.now())
            }
            
            self.logger.log_info("Relatório de visitantes gerado")
            return {'sucesso': True, 'relatorio': relatorio}
            
        except Exception as e:
            self.logger.log_erro("Erro ao gerar relatório de visitantes", e)
            return {'sucesso': False, 'mensagem': str(e)}
    
    def _calcular_estatisticas(self) -> Dict:
        """Calcula estatísticas de visitantes"""
        total = len(self.zoo.visitantes)
        criancas = sum(1 for v in self.zoo.visitantes if v.idade < 12)
        idosos = sum(1 for v in self.zoo.visitantes if v.idade >= 60)
        
        return {
            'total': total,
            'criancas': criancas,
            'adultos': total - criancas - idosos,
            'idosos': idosos,
            'arrecadacao': sum(i.valor for i in self.zoo.ingressos)
        }