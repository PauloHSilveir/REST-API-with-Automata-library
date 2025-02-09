from typing import List, Tuple, Dict, Set
from pydantic import BaseModel, validator
from fastapi import HTTPException

class NTMModel(BaseModel):
    states: List[str]
    input_symbols: Set[str]
    tape_symbols: Set[str]
    transitions: Dict[str, Dict[str, List[Tuple[str, str, str]]]]
    initial_state: str
    blank_symbol: str
    final_states: Set[str]

    @validator("transitions")
    def validate_transitions(cls, transitions, values):
        states = values.get("states", set())
        tape_symbols = values.get("tape_symbols", set())
        valid_directions = values.get("valid_directions", {"L", "R"})
        final_states = values.get("final_states", set())

        for state, symbol_transitions in transitions.items():
            if state not in states:
                raise HTTPException(status_code=400, detail=f"InvalidStateError: State {state} is not in states set")

            for symbol, transitions_list in symbol_transitions.items():
                if symbol not in tape_symbols:
                    raise HTTPException(status_code=400, detail=f"InvalidSymbolError: Symbol {symbol} is not in tape symbols")

                for next_state, write_symbol, direction in transitions_list:
                    if next_state not in states:
                        raise HTTPException(status_code=400, detail=f"InvalidStateError: Next state {next_state} is not in states set")

                    if write_symbol not in tape_symbols:
                        raise HTTPException(status_code=400, detail=f"InvalidSymbolError: Write symbol {write_symbol} is not in tape symbols")

                    if direction not in valid_directions:
                        raise HTTPException(status_code=400, detail=f"InvalidDirectionError: Direction {direction} is not valid")

            if state in final_states and symbol_transitions:
                raise HTTPException(status_code=400, detail=f"FinalStateError: Transitions found for final state {state}")

        return transitions