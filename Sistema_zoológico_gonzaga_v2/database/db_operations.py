from . import load_db, save_db
from datetime import datetime

class DBOperations:
    @staticmethod
    def get_all_animais():
        data = load_db()
        return data.get("animais", [])
    
    @staticmethod
    def add_animal(animal_data):
        data = load_db()
        data["animais"].append(animal_data)
        save_db(data)
        return True
    
    @staticmethod
    def update_animal(nome, new_data):
        data = load_db()
        for animal in data["animais"]:
            if animal["nome"] == nome:
                animal.update(new_data)
                save_db(data)
                return True
        return False
    
    @staticmethod
    def delete_animal(nome):
        data = load_db()
        data["animais"] = [a for a in data["animais"] if a["nome"] != nome]
        save_db(data)
        return True
    
    # Operações similares para habitats
    @staticmethod
    def get_all_habitats():
        data = load_db()
        return data.get("habitats", [])
    
    @staticmethod
    def add_habitat(habitat_data):
        data = load_db()
        data["habitats"].append(habitat_data)
        save_db(data)
        return True
    
    # Operações para visitantes
    @staticmethod
    def get_all_visitantes():
        data = load_db()
        return data.get("visitantes", [])
    
    @staticmethod
    def add_visitante(visitante_data):
        data = load_db()
        data["visitantes"].append(visitante_data)
        save_db(data)
        return True
    
    # Operações para ingressos
    @staticmethod
    def get_all_ingressos():
        data = load_db()
        return data.get("ingressos", [])
    
    @staticmethod
    def add_ingresso(ingresso_data):
        data = load_db()
        data["ingressos"].append(ingresso_data)
        save_db(data)
        return True
    
    @staticmethod
    def get_next_id(tipo):
        """Gera IDs sequenciais simples"""
        data = load_db()
        if tipo == "visitante":
            existing = [v["id_visitante"] for v in data["visitantes"]]
            prefix = "VIS"
        elif tipo == "ingresso":
            existing = [i["codigo"] for i in data["ingressos"]]
            prefix = "ING"
        else:
            return None
        
        if not existing:
            return f"{prefix}001"
        
        last_num = max(int(id.replace(prefix, "")) for id in existing)
        return f"{prefix}{last_num + 1:03d}"