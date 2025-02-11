from typing import List, Dict, Set, Tuple
from pydantic import BaseModel, validator

class DPDAModel(BaseModel):
    states: Set[str]
    input_symbols: Set[str]
    stack_symbols: Set[str]
    transitions: Dict[str, Dict[str, Dict[str, Tuple[str, Tuple[str, ...]]]]]
    initial_state: str
    initial_stack_symbol: str
    final_states: Set[str]
    acceptance_mode: str

    @validator('initial_state')
    def initial_state_must_be_valid(cls, v, values):
        if 'states' in values and v not in values['states']:
            raise ValueError('initial_state must be one of the states')
        return v

    @validator('initial_stack_symbol')
    def initial_stack_symbol_must_be_valid(cls, v, values):
        if 'stack_symbols' in values and v not in values['stack_symbols']:
            raise ValueError('initial_stack_symbol must be one of the stack symbols')
        return v

    @validator('final_states', each_item=True)
    def final_states_must_be_valid(cls, v, values):
        if 'states' in values and v not in values['states']:
            raise ValueError('Each final_state must be one of the states')
        return v

    @validator('transitions')
    def transitions_must_be_valid(cls, v, values):
        if 'states' in values and 'input_symbols' in values and 'stack_symbols' in values:
            for state, paths in v.items():
                if state not in values['states']:
                    raise ValueError(f'Transition state {state} must be one of the states')
                for symbol, stack_paths in paths.items():
                    if symbol not in values['input_symbols']:
                        raise ValueError(f'Transition symbol {symbol} must be one of the input symbols')
                    for stack_symbol, (next_state, stack_action) in stack_paths.items():
                        if stack_symbol not in values['stack_symbols']:
                            raise ValueError(f'Transition stack symbol {stack_symbol} must be one of the stack symbols')
                        if next_state not in values['states']:
                            raise ValueError(f'Transition next state {next_state} must be one of the states')
                        for action in stack_action:
                            if action not in values['stack_symbols'] and action != '':
                                raise ValueError(f'Transition stack action {action} must be one of the stack symbols or empty')
        return v