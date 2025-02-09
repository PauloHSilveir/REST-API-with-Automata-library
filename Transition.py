from pydantic import BaseModel

class Transition(BaseModel):
    next_state: str
    write_symbol: str
    direction: str