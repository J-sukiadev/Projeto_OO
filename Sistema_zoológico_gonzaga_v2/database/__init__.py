"""
Módulo de persistência de dados do sistema de zoológico

Responsável por:
- Gerenciamento do arquivo JSON principal
- Backups automáticos
- Versionamento de dados
"""

import json
import os
from datetime import datetime
from pathlib import Path
import shutil
from typing import Dict, Any

# Configurações
DB_FOLDER = Path(__file__).parent
MAIN_DB = DB_FOLDER / "zoo_db.json"
BACKUP_FOLDER = DB_FOLDER / "backups"
MAX_BACKUPS = 5

def criar_estrutura_inicial():
    """Cria a estrutura de arquivos e pastas se não existir"""
    try:
        BACKUP_FOLDER.mkdir(exist_ok=True)
        
        if not MAIN_DB.exists():
            with open(MAIN_DB, 'w', encoding='utf-8') as f:
                json.dump({
                    "nome": "Zoológico Virtual",
                    "habitats": [],
                    "animais": [],
                    "visitantes": [],
                    "ingressos": [],
                    "metadata": {
                        "versao": "1.0",
                        "ultima_atualizacao": datetime.now().isoformat()
                    }
                }, f, indent=2)
                
    except Exception as e:
        raise RuntimeError(f"Falha ao criar estrutura inicial: {str(e)}")

def carregar_dados() -> Dict[str, Any]:
    """Carrega os dados do arquivo JSON principal com tratamento de erros"""
    try:
        criar_estrutura_inicial()
        
        with open(MAIN_DB, 'r', encoding='utf-8') as f:
            dados = json.load(f)
            
            # Validação básica da estrutura
            if not all(key in dados for key in ["nome", "habitats", "animais", "visitantes"]):
                raise ValueError("Estrutura do arquivo JSON inválida")
                
            return dados
            
    except FileNotFoundError:
        raise FileNotFoundError("Arquivo de banco de dados não encontrado")
    except json.JSONDecodeError:
        raise ValueError("Arquivo de banco de dados corrompido")
    except Exception as e:
        raise RuntimeError(f"Erro ao carregar dados: {str(e)}")

def salvar_dados(dados: Dict[str, Any]):
    """Salva os dados no arquivo JSON principal com backup automático"""
    try:
        criar_estrutura_inicial()
        
        # Adiciona metadados
        dados["metadata"] = {
            "versao": "1.0",
            "ultima_atualizacao": datetime.now().isoformat()
        }
        
        # Cria backup antes de salvar
        criar_backup()
        
        # Salva os dados principais
        with open(MAIN_DB, 'w', encoding='utf-8') as f:
            json.dump(dados, f, indent=2, ensure_ascii=False)
            
    except Exception as e:
        raise RuntimeError(f"Erro ao salvar dados: {str(e)}")

def criar_backup():
    """Cria um backup rotativo do arquivo de dados"""
    try:
        if not MAIN_DB.exists():
            return
            
        # Formato: backup_YYYYMMDD_HHMMSS.json
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = BACKUP_FOLDER / f"backup_{timestamp}.json"
        
        shutil.copy(MAIN_DB, backup_file)
        
        # Limita o número de backups
        backups = sorted(BACKUP_FOLDER.glob("backup_*.json"), key=os.path.getmtime)
        if len(backups) > MAX_BACKUPS:
            for old_backup in backups[:-MAX_BACKUPS]:
                old_backup.unlink()
                
    except Exception as e:
        raise RuntimeError(f"Falha ao criar backup: {str(e)}")

def restaurar_backup(backup_file: str):
    """Restaura um backup específico"""
    try:
        backup_path = BACKUP_FOLDER / backup_file
        if not backup_path.exists():
            raise FileNotFoundError("Arquivo de backup não encontrado")
            
        shutil.copy(backup_path, MAIN_DB)
        return True
        
    except Exception as e:
        raise RuntimeError(f"Falha ao restaurar backup: {str(e)}")