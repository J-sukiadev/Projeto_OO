from datetime import datetime
from typing import Dict
from package.models.animal import Mamifero, Ave, Reptil
from package.utils import Logger, Helpers

class RelatorioService:
    def __init__(self, zoo, logger: Logger):
        # Inicialização simples, recebendo as dependências necessárias
        # O zoo contém todos os dados e o logger vai registrar as operações
        self.zoo = zoo
        self.logger = logger
    
    def gerar_relatorio_geral(self) -> Dict:
        """Gera um relatório consolidado do zoológico"""
        try:
            # Estrutura bem organizada, separando por categorias
            relatorio = {
                'animais': self._relatorio_animais(),  # Seção de animais
                'habitats': self._relatorio_habitats(),  # Seção de habitats
                'visitantes': self._relatorio_visitantes(),  # Seção de visitantes
                'data_geracao': Helpers.formatar_data(datetime.now())  # Data formatada
            }
            
            self.logger.log_info("Relatório geral gerado")  # Registro no log
            return {'sucesso': True, 'relatorio': relatorio}  # Retorno padronizado
            
        except Exception as e:
            # Tratamento de erro completo com logging
            self.logger.log_erro("Erro ao gerar relatório geral", e)
            return {'sucesso': False, 'mensagem': str(e)}  # Retorno de erro consistente
    
    def _relatorio_animais(self) -> Dict:
        """Gera seção de animais do relatório"""
        # Contagem inteligente por tipo usando isinstance
        total = len(self.zoo.animais)
        tipos = {
            'Mamíferos': sum(1 for a in self.zoo.animais if isinstance(a, Mamifero)),
            'Aves': sum(1 for a in self.zoo.animais if isinstance(a, Ave)),
            'Répteis': sum(1 for a in self.zoo.animais if isinstance(a, Reptil))
        }
        
        # Estrutura de dados clara e bem organizada
        return {
            'total': total,
            'tipos': tipos,  # Dicionário com contagem por tipo
            'alimentados': sum(1 for a in self.zoo.animais if a.alimentado)  # Status útil
        }
    
    def _relatorio_habitats(self) -> Dict:
        """Gera seção de habitats do relatório"""
        # Uso de comprehensions para cálculos concisos
        return {
            'total': len(self.zoo.habitats),
            'capacidade_total': sum(h.capacidade for h in self.zoo.habitats),
            # Mapeamento claro de animais por habitat
            'animais_por_habitat': {
                h.nome: len(h.animais) for h in self.zoo.habitats
            }
        }
    
    def _relatorio_visitantes(self) -> Dict:
        """Gera seção de visitantes do relatório"""
        total = len(self.zoo.visitantes)
        ingressos = len(self.zoo.ingressos)
        
        # Cálculo financeiro incluído diretamente
        return {
            'total_visitantes': total,
            'total_ingressos': ingressos,
            # Proteção contra divisão por zero
            'media_visitas': ingressos / total if total > 0 else 0,
            'arrecadacao_total': sum(i.valor for i in self.zoo.ingressos)  # Soma dos valores
        }
    
    def exportar_relatorio(self, tipo: str, arquivo: str) -> Dict:
        """Exporta relatório para arquivo"""
        try:
            # Seleção do tipo de relatório com tratamento de erro
            if tipo == 'Animais':
                dados = self._relatorio_animais()
            elif tipo == 'Habitats':
                dados = self._relatorio_habitats()
            elif tipo == 'Visitantes':
                dados = self._relatorio_visitantes()
            else:
                return {'sucesso': False, 'mensagem': 'Tipo de relatório inválido'}
            
            # Criação segura de diretórios se não existirem
            import os
            os.makedirs(os.path.dirname(arquivo), exist_ok=True)
            
            # Escrita do arquivo JSON com formatação
            with open(arquivo, 'w', encoding='utf-8') as f:
                import json
                json.dump(dados, f, indent=2, ensure_ascii=False)  # Bem formatado
            
            self.logger.log_info(f"Relatório {tipo} exportado para {arquivo}")
            return {'sucesso': True, 'arquivo': arquivo}  # Feedback útil
            
        except Exception as e:
            # Log detalhado do erro
            self.logger.log_erro(f"Erro ao exportar relatório {tipo}", e)
            return {'sucesso': False, 'mensagem': str(e)}  # Mensagem de erro clara