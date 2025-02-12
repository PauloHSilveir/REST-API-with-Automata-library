from typing import List, Dict, Set
from pydantic import BaseModel, validator
from fastapi import HTTPException

class DFAModel(BaseModel):
    states: List[str]
    input_symbols: List[str]
    transitions: Dict[str, Dict[str, str]]
    initial_state: str
    final_states: List[str]

    @validator('initial_state')
    def initial_state_must_be_valid(cls, v, values):
        if 'states' in values and v not in values['states']:
            raise ValueError('initial_state must be one of the states')
        return v

    @validator('final_states', each_item=True)
    def final_states_must_be_valid(cls, v, values):
        if 'states' in values and v not in values['states']:
            raise ValueError('Each final_state must be one of the states')
        return v

    @validator('transitions')
    def transitions_must_be_valid(cls, v, values):
        if 'states' in values and 'input_symbols' in values:
            for state, paths in v.items():
                if state not in values['states']:
                    raise ValueError(f'Transition state {state} must be one of the states')
                for symbol, next_state in paths.items():
                    if symbol not in values['input_symbols']:
                        raise ValueError(f'Transition symbol {symbol} must be one of the input symbols')
                    if next_state not in values['states']:
                        raise ValueError(f'Transition next state {next_state} must be one of the states')
        return v