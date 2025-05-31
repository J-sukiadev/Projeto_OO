# Relações de Orientação a Objetos
# Usar isso como base para o Projeto livre



# ------------------>>Relação de Herança<<-------------------------------------------------
# --uma classe herda características da outra--

class Animal:
    def mover(self):
        print("Movendo-se")

class Cachorro(Animal):  # Cachorro É UM Animal
    def latir(self):
        print("Au au!")

# ------------------>>Relação de Polimorfismo<<-------------------------------------------
# --relação onde um objeto pode ser referenciado de várias formas--

meu_animal = Cachorro()  # Polimorfismo
meu_animal.mover()  # Chama o método de Animal
# meu_animal.latir()  # Funciona porque é um Cachorro

             #>>>>Com métodos sobrescritos:<<<<
class Animal:
    def emitir_som(self):
        print("Som genérico")

class Gato(Animal):
    def emitir_som(self):  # Sobrescrita de método
        print("Miau!")

animal = Gato()
animal.emitir_som()  # Saída: Miau! - polimorfismo em ação

# ------------------->>Relação de Associação<<---------------------------------------
# --Relacionamento "tem um" entre objetos:--
# 1. Associação simples:

class Professor:
    def __init__(self):
        self.departamento = None  # Professor TEM UM Departamento

class Departamento:
    def __init__(self, nome):
        self.nome = nome

# 2. Agregação:
# --(Todo-Parte, relação estruturada fraca)

class Turma:
    def __init__(self):
        self.alunos = []  # Turma TEM alunos
    
    def adicionar_aluno(self, aluno):
        self.alunos.append(aluno)
    # Se a turma for destruída, os alunos continuam existindo

class Aluno:
    def __init__(self, nome):
        self.nome = nome

# 3. Composiçao:
# --(Todo-Parte, relação estruturada forte)

class Carro:
    def __init__(self):
        self.motor = Motor()  # Carro TEM UM Motor (criado junto)
    # Se o carro for destruído, o motor também será

class Motor:
    def ligar(self):
        print("Motor ligado")

# ------------------>>Relação de Uso<<-------------------------------------------------
#Ocorre quando uma classe usa temporariamente outra, sem manter uma referência permanente.

class Logger:
    def log(self, message):
        print(f"LOG: {message}")

class Processador:
    def processar(self, dados, logger):  # Dependência injetada
        logger.log("Iniciando processamento")
        # ... processamento ...
        logger.log("Processamento concluído")

# Uso:
logger = Logger()
processador = Processador()
processador.processar([1, 2, 3], logger)  # Relação temporária

# ---------------------->>Relação de dependência<<------------------------------
# --Relação mais fraca onde uma classe usa outra temporariamente.--

class Relatorio:
    def gerar(self, impressora):  # Relatório DEPENDE de Impressora
        impressora.imprimir(self)

class Impressora:
    def imprimir(self, relatorio):
        print("Imprimindo relatório...")

# ---------------------->>Relação de Cardinalidade<<------------------------------
#Indica quantos objetos participam de uma relação.

class Biblioteca:
    def __init__(self):
        self.livros = []  # 1 Biblioteca para N Livros (1:N)

class Livro:
    def __init__(self, titulo):
        self.titulo = titulo

# Uso:
bib = Biblioteca()
bib.livros.append(Livro("Dom Casmurro"))
bib.livros.append(Livro("1984"))

# -------------------->>Relação de interface<<----------------------------------
# --Em Python usamos classes abstratas (ABC) ou duck typing para interfaces.--

from abc import ABC, abstractmethod

class Autenticavel(ABC):  # Interface
    @abstractmethod
    def autenticar(self, senha):
        pass

class Usuario(Autenticavel):  # Usuario REALIZA Autenticavel
    def autenticar(self, senha):
        # implementação
        return True

class Sistema:
    def login(self, autenticavel: Autenticavel):  # Polimorfismo com interface
        autenticavel.autenticar("123")

# Versão com Duck Typing (mais pythonico):

# Não precisa herdar explicitamente, apenas implementar os métodos necessários
class Usuario:
    def autenticar(self, senha):
        return senha == "1234"

class Sistema:
    def login(self, autenticavel):  # Qualquer objeto com método autenticar() funciona
        if autenticavel.autenticar("1234"):
            print("Acesso concedido")
        else:
            print("Acesso negado")

