# Sistema de Gerenciamento de Zoológico

Sistema completo para gerenciamento de zoológicos com interface gráfica, persistência de dados e relatórios.

## Funcionalidades Principais

### Gerenciamento de Animais
- **Cadastro completo**: Registre mamíferos, aves e répteis com atributos específicos
- **Controle de habitats**: Associe animais aos habitats adequados
- **Alimentação**: Registre e acompanhe a dieta dos animais
- **Busca e filtros**: Listagem organizada por tipo, habitat ou nome

### Gerenciamento de Habitats
- **Cadastro flexível**: Crie habitats com capacidades personalizadas
- **Monitoramento**: Acompanhe lotação e disponibilidade
- **Compatibilidade**: Sistema previne alocação inadequada

### Gerenciamento de Visitantes
- **Registro ágil**: Cadastro rápido de visitantes
- **Sistema de ingressos**: Geração automática com cálculos de desconto
- **Histórico**: Registro completo de visitas

### Relatórios e Análises
- **Dashboard integrado**: Visualização rápida de estatísticas
- **Relatórios detalhados**:
  - Inventário de animais
  - Capacidade de habitats
  - Movimentação financeira
  - Perfil de visitantes

## 🛠️ Tecnologias e Padrões
- **POO Avançada**: 
  - Herança (`Animal → Mamifero/Ave/Reptil`)
  - Polimorfismo
  - Composição
  - Associação fraca
- **Persistência**: 
  - Armazenamento em JSON
  - Sistema de backup automático
- **Interface**: 
  - Tkinter com estilos modernos
  - Layout responsivo

## 🚀 Como Executar

1. **Pré-requisitos**:
   ```bash
   Python 3.10+

2. **Instalação**:
git clone [eu não sei como colocar o link]
cd Sistema_zoológico_gonzaga_v2

3. **Execução**:
python main.py


## Estrutura do projeto:
Sistema_zoológico_gonzaga_v2/
├── database/               # Armazenamento persistente
│   └── zoo_db.json         # Dados em formato JSON
│
├── package/                # Lógica principal
│   ├── models/             # Entidades do sistema
│   ├── services/           # Regras de negócio
│   └── utils/              # Utilitários
│
├── views/                  # Interface gráfica
│   ├── animais_view.py     # Gerenciamento de animais
│   ├── habitats_view.py    # Controle de habitats
│   ├── visitantes_view.py  # Cadastro de visitantes
│   └── relatorios_view.py  # Geração de relatórios
│
├── main.py                 # Ponto de entrada
└── README.md               # Documentação

