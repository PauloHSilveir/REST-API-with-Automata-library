# REST API with Automata Library

Trabalho para a disciplina de Teoria da Computação da Universidade Federal de Lavras. Construção de uma API REST para representação de autômatos.

## Automaton Creator

Este projeto permite criar e visualizar autômatos (DFA, DPDA, NTM) usando uma interface gráfica Tkinter e uma API FastAPI.

## Configuração e Execução do Projeto

### Pré-requisitos

- Python 3.8 ou superior
- Pip (gerenciador de pacotes do Python)

### Instalação

1. Clone o repositório:

   ```bash
   git clone https://github.com/seu-usuario/automaton-creator.git
   cd automaton-creator
   ```

2. Crie um ambiente virtual:

   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows, use `venv\Scripts\activate`
   ```

3. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

### Execução

1. Inicie o servidor FastAPI:

   ```bash
   uvicorn server:app --reload
   ```

2. Em uma nova janela do terminal, execute a interface gráfica Tkinter:

   ```bash
   python main.py
   ```

### Endpoints de Acesso

- **Interface Frontend:** [http://localhost:3000](http://localhost:3000)
- **Documentação Swagger:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **Documentação ReDoc:** [http://localhost:8000/redoc](http://localhost:8000/redoc)

## Exemplos de Uso da API

### Criar um NTM
Exemplo: Criar uma Máquina de Turing que aceita 0^n 1^n.

#### Requisição:

```json
POST /ntm/
{
  "ntm": {
    "states": ["q0", "q1", "q2", "q3", "q4"],
    "input_symbols": ["0", "1"],
    "tape_symbols": ["0", "1", "x", "y", "."],
    "transitions": {
        "q0": {"0": [["q1", "x", "R"]], "y": [["q3", "y", "R"]]},
        "q1": {"0": [["q1", "0", "R"]], "1": [["q2", "y", "L"]], "y": [["q1", "y", "R"]]},
        "q2": {"0": [["q2", "0", "L"]], "x": [["q0", "x", "R"]], "y": [["q2", "y", "L"]]},
        "q3": {"y": [["q3", "y", "R"]], ".": [["q4", ".", "R"]]}
    },
    "initial_state": "q0",
    "blank_symbol": ".",
    "final_states": ["q4"],
    "valid_directions": ["L", "R"]
  }
}
```

### Criar um DFA
Exemplo: Criar um AFD que aceita um número ímpar de `1`s.

#### Requisição:

```json
POST /dfa/
{
  "dfa": {
    "states": ["q0", "q1", "q2"],
    "input_symbols": ["0", "1"],
    "transitions": {
      "q0": {"0": "q0", "1": "q1"},
      "q1": {"0": "q0", "1": "q2"},
      "q2": {"0": "q2", "1": "q1"}
    },
    "initial_state": "q0",
    "final_states": ["q1"]
  }
}
```

### Criar um DPDA
Exemplo: Criar um DPDA que aceita a^n b^n >= 1.

#### Requisição:

```json
POST /dpda/
{
  "dpda": {
    "states": ["q0", "q1", "q2", "q3"],
    "input_symbols": ["a", "b"],
    "stack_symbols": ["0", "1"],
    "transitions": {
      "q0": {"a": {"0": ["q1", ["1", "0"]]}},
      "q1": {"a": {"1": ["q1", ["1", "1"]]}, "b": {"1": ["q2", ""]}},
      "q2": {"b": {"1": ["q2", ""]}, "": {"0": ["q3", ["0"]]}}
    },
    "initial_state": "q0",
    "initial_stack_symbol": "0",
    "final_states": ["q3"],
    "acceptance_mode": "final_state"
  }
}
```

## API Endpoints

### Geração e Validação
- `GET /automaton_image/{automaton_id}`: Gera representação visual do autômato.
- `POST /validate_input/{automaton_id}`: Testa aceitação de cadeias.

### AFD (DFA)
- `POST /dfa/`: Criar novo DFA.
- `GET /dfa/{dfa_id}`: Obter detalhes do DFA.

### PDA (DPDA)
- `POST /dpda/`: Criar novo DPDA.
- `GET /dpda/{dpda_id}`: Obter detalhes do DPDA.

### Máquina de Turing (NTM)
- `POST /ntm/`: Criar nova NTM.
- `GET /ntm/{ntm_id}`: Obter detalhes da NTM.

## Estrutura do Projeto

```
/REST-API-with-Automata-library/
├── main.py
├── server.py
├── gui/
│   ├── menu.py
│   ├── parsers.py
│   └── submitters.py
├── visualizers.py
├── routes/
│   ├── routes.py
│   ├── data_utils.py
│   └── visualizers.py
├── models/
│   ├── NTMModel.py
│   ├── DFAModel.py
│   ├── DPDAModel.py
│   └── InputValidationRequest.py
├── automato/
│   ├── ntm_visualizer.py
│   ├── dfa_visualizer.py
│   └── dpda_visualizer.py
├── data/
└── output/
```

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e pull requests.

## Licença

Este projeto está licenciado sob a Licença MIT. Veja o arquivo LICENSE para mais detalhes.
