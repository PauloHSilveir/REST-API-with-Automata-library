# filepath: /home/paulo/Documentos/REST-API-with-Automata-library/routes.py
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from models.NTMModel import NTMModel
from models.DFAModel import DFAModel
from models.DPDAModel import DPDAModel
from models.InputValidationRequest import InputValidationRequest
from automata.fa.dfa import DFA
from automata.pda.dpda import DPDA
from automata.tm.ntm import NTM
from routes.data_utils import read_data, write_data, DATA_DIR, OUTPUT_DIR
from routes.visualizers import generate_automaton_image
import uuid
import os

router = APIRouter()

@router.get("/")
async def read_root():
    return {"Hello": "World"}

@router.get("/ntm/{ntm_id}")
async def get_ntm(ntm_id: str):
    file_path = os.path.join(DATA_DIR, f"{ntm_id}.json")
    data = await read_data(file_path)
    if not data:
        raise HTTPException(status_code=404, detail="NTM data not found")
    return data

@router.get("/dfa/{dfa_id}")
async def get_dfa(dfa_id: str):
    file_path = os.path.join(DATA_DIR, f"{dfa_id}.json")
    data = await read_data(file_path)
    if not data:
        raise HTTPException(status_code=404, detail="DFA data not found")
    return data

@router.get("/dpda/{dpda_id}")
async def get_dpda(dpda_id: str):
    file_path = os.path.join(DATA_DIR, f"{dpda_id}.json")
    data = await read_data(file_path)
    if not data:
        raise HTTPException(status_code=404, detail="DPDA data not found")
    return data

@router.post("/ntm/")
async def receive_ntm(ntm_data: NTMModel):
    ntm_id = str(uuid.uuid4())
    file_path = os.path.join(DATA_DIR, f"{ntm_id}.json")
    await write_data(file_path, ntm_data.dict())
    generate_automaton_image(ntm_data.dict(), ntm_id)
    return {
        "message": "NTM received successfully", 
        "id": ntm_id,
        "data": ntm_data
    }

@router.post("/dfa/")
async def receive_dfa(dfa_data: DFAModel):
    dfa_id = str(uuid.uuid4())
    file_path = os.path.join(DATA_DIR, f"{dfa_id}.json")
    await write_data(file_path, dfa_data.dict())
    generate_automaton_image(dfa_data.dict(), dfa_id)
    return {
        "message": "DFA received successfully", 
        "id": dfa_id,
        "data": dfa_data
    }

@router.post("/dpda/")
async def receive_dpda(dpda_data: DPDAModel):
    dpda_id = str(uuid.uuid4())
    file_path = os.path.join(DATA_DIR, f"{dpda_id}.json")
    await write_data(file_path, dpda_data.dict())
    generate_automaton_image(dpda_data.dict(), dpda_id)
    return {
        "message": "DPDA received successfully", 
        "id": dpda_id,
        "data": dpda_data
    }

@router.get("/automaton_image/{automaton_id}")
async def get_automaton_image(automaton_id: str):
    file_path = os.path.join(OUTPUT_DIR, f"{automaton_id}.png")
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Automaton image not found")
    return FileResponse(file_path)

@router.post("/validate_input/{automaton_id}")
async def validate_input(automaton_id: str, request: InputValidationRequest):
    file_path = os.path.join(DATA_DIR, f"{automaton_id}.json")

    data = await read_data(file_path) 
    if not data:
        raise HTTPException(status_code=404, detail="Automaton data not found")
    
    data["final_states"] = set(data["final_states"])
    data["states"] = set(data["states"])
    if "tape_symbols" in data:
        automaton = NTM(**data)
    elif "stack_symbols" in data:
        automaton = DPDAModel(**data)
    else:
        automaton = DFA(**data)

    # Validação da string de entrada
    is_accepted = automaton.accepts_input(request.input_str)
    return {"input": request.input_str, "accepted": is_accepted}