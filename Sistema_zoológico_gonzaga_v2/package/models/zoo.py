from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime
import json
import os
from .animal import Animal, Mamifero, Ave, Reptil
from .habitat import Habitat
from .visitante import Visitante, Ingresso

class Zoo:
    """Classe principal que representa o zoológico"""
    
    def __init__(self, nome: str):
        self.nome: str = nome
        self.habitats: List[Habitat] = []
        self.animais: List[Animal] = []
        self.visitantes: List[Visitante] = []
        self.ingressos: List[Ingresso] = []
    
    def adicionar_habitat(self, habitat: Habitat) -> None:
        """Adiciona um novo habitat ao zoológico"""
        self.habitats.append(habitat)
    
    def adicionar_animal(self, animal: Animal, habitat_nome: str) -> bool:
        """Adiciona animal ao habitat especificado"""
        self.animais.append(animal)
        for habitat in self.habitats:
            if habitat.nome == habitat_nome:
                return habitat.adicionar_animal(animal)
        return False
    
    def registrar_visita(self, visitante: Visitante) -> Ingresso:
        """Registra uma nova visita e retorna o ingresso"""
        self.visitantes.append(visitante)
        ingresso = Ingresso(visitante, datetime.now())
        self.ingressos.append(ingresso)
        return ingresso
    
    def salvar_estado(self, arquivo: str) -> None:
        """Salva o estado atual do zoológico em arquivo JSON"""
        try:
            estado = {
                'nome': self.nome,
                'habitats': [{
                    'nome': h.nome,
                    'tipo': h.tipo,
                    'capacidade': h.capacidade,
                    'animais': [a.nome for a in h.animais]
                } for h in self.habitats],
                'animais': [{
                    'nome': a.nome,
                    'especie': a.especie,
                    'idade': a.idade,
                    'tipo': a.__class__.__name__,
                    'detalhes': self._obter_detalhes_animal(a)
                } for a in self.animais],
                'visitantes': [{
                    'nome': v.nome,
                    'idade': v.idade,
                    'id_visitante': v.id_visitante
                } for v in self.visitantes],
                'ingressos': [{
                    'codigo': i.codigo,
                    'valor': i.valor,
                    'data': i.data.isoformat(),
                    'id_visitante': i.visitante.id_visitante
                } for i in self.ingressos]
            }
            
            os.makedirs(os.path.dirname(arquivo), exist_ok=True)
            
            with open(arquivo, 'w', encoding='utf-8') as f:
                json.dump(estado, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            raise Exception(f"Erro ao salvar estado: {str(e)}")
    
    def _obter_detalhes_animal(self, animal: Animal) -> Dict:
        """Retorna detalhes específicos do tipo de animal"""
        if isinstance(animal, Mamifero):
            return {'pelagem': animal.pelagem}
        elif isinstance(animal, Ave):
            return {'envergadura': animal.envergadura_asas}
        elif isinstance(animal, Reptil):
            return {'escamas': animal.escamas}
        return {}
    
    def carregar_estado(self, arquivo: str) -> bool:
        """Carrega o estado do zoológico de um arquivo JSON"""
        try:
            with open(arquivo, 'r', encoding='utf-8') as f:
                estado = json.load(f)
            
            # Limpa estado atual
            self.habitats = []
            self.animais = []
            self.visitantes = []
            self.ingressos = []
            
            self.nome = estado.get('nome', self.nome)
            
            # 1. Cria habitats
            habitats_data = estado.get('habitats', [])
            self.habitats = [Habitat(h['nome'], h['tipo'], h['capacidade']) 
                           for h in habitats_data]
            
            # 2. Cria animais e mapeia por nome
            animais_map = {}
            for a in estado.get('animais', []):
                animal = self._criar_animal_por_tipo(a)
                if animal:
                    self.animais.append(animal)
                    animais_map[a['nome']] = animal
            
            # 3. Associa animais aos habitats
            for h_data, habitat in zip(habitats_data, self.habitats):
                for nome_animal in h_data.get('animais', []):
                    if nome_animal in animais_map:
                        habitat.adicionar_animal(animais_map[nome_animal])
            
            # 4. Carrega visitantes e mapeia por ID
            visitantes_map = {}
            for v in estado.get('visitantes', []):
                visitante = Visitante(v['nome'], v['idade'], v['id_visitante'])
                self.visitantes.append(visitante)
                visitantes_map[v['id_visitante']] = visitante
            
            # 5. Carrega ingressos
            for i in estado.get('ingressos', []):
                if i['id_visitante'] in visitantes_map:
                    ingresso = Ingresso(
                        visitantes_map[i['id_visitante']],
                        datetime.fromisoformat(i['data'])
                    )
                    ingresso.codigo = i['codigo']
                    ingresso.valor = i['valor']
                    self.ingressos.append(ingresso)
            
            return True
            
        except FileNotFoundError:
            return False
        except Exception as e:
            raise Exception(f"Erro ao carregar estado: {str(e)}")
    
    def _criar_animal_por_tipo(self, dados: Dict) -> Optional[Animal]:
        """Factory method para criar animais baseado no tipo"""
        tipo = dados.get('tipo', '')
        detalhes = dados.get('detalhes', {})
        
        if tipo == 'Mamifero':
            return Mamifero(
                dados['nome'],
                dados['especie'],
                dados['idade'],
                detalhes.get('pelagem', 'curta')
            )
        elif tipo == 'Ave':
            return Ave(
                dados['nome'],
                dados['especie'],
                dados['idade'],
                detalhes.get('envergadura', 1.0)
            )
        elif tipo == 'Reptil':
            return Reptil(
                dados['nome'],
                dados['especie'],
                dados['idade'],
                detalhes.get('escamas', 'escamosas')
            )
        return None
    
    def __str__(self) -> str:
        return (f"Zoológico {self.nome}\n"
                f"Habitats: {len(self.habitats)}\n"
                f"Animais: {len(self.animais)}\n"
                f"Visitantes: {len(self.visitantes)}")