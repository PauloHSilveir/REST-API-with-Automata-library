from pydantic import BaseModel

class InputValidationRequest(BaseModel):
    input_str: str