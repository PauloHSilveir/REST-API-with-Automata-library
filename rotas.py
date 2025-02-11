# filepath: /home/paulo/Documentos/REST-API-with-Automata-library/rotas.py
from typing import Union
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from models.NTMModel import NTMModel  # Import NTMModel
from models.InputValidationRequest import InputValidationRequest 
from models.DFAModel import DFAModel  # Import DFAModel
from models.DPDAModel import DPDAModel  # Import DPDAModel
from automato.ntm_visualizer import draw_ntm, load_automaton
from automata.fa.dfa import DFA
from automata.tm.ntm import NTM
import json
import os
import uuid
import aiofiles
import asyncio

app = FastAPI()

DATA_DIR = "data"
OUTPUT_DIR = "output"

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

async def read_data(file_path):
    if not os.path.exists(file_path):
        return {}
    async with aiofiles.open(file_path, "r") as file:
        content = await file.read()
        return json.loads(content)

async def write_data(file_path, data):
    async with aiofiles.open(file_path, "w") as file:
        await file.write(json.dumps(data, indent=4))
    await asyncio.sleep(0.1)  # Adiciona um pequeno atraso para garantir que a escrita seja concluída

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/ntm/{ntm_id}")
async def get_ntm(ntm_id: str):
    file_path = os.path.join(DATA_DIR, f"{ntm_id}.json")
    data = await read_data(file_path)
    if not data:
        raise HTTPException(status_code=404, detail="NTM data not found")
    return data

@app.get("/dfa/{dfa_id}")
async def get_dfa(dfa_id: str):
    file_path = os.path.join(DATA_DIR, f"{dfa_id}.json")
    data = await read_data(file_path)
    if not data:
        raise HTTPException(status_code=404, detail="DFA data not found")
    return data

@app.get("/dpda/{dpda_id}")
async def get_dpda(dpda_id: str):
    file_path = os.path.join(DATA_DIR, f"{dpda_id}.json")
    data = await read_data(file_path)
    if not data:
        raise HTTPException(status_code=404, detail="DPDA data not found")
    return data

@app.post("/ntm/")
async def receive_ntm(ntm_data: NTMModel):
    ntm_id = str(uuid.uuid4())
    file_path = os.path.join(DATA_DIR, f"{ntm_id}.json")
    await write_data(file_path, ntm_data.dict())
    return {
        "message": "NTM received successfully", 
        "id": ntm_id,
        "data": ntm_data
    }

@app.post("/dfa/")
async def receive_dfa(dfa_data: DFAModel):
    dfa_id = str(uuid.uuid4())
    file_path = os.path.join(DATA_DIR, f"{dfa_id}.json")
    await write_data(file_path, dfa_data.dict())
    return {
        "message": "DFA received successfully", 
        "id": dfa_id,
        "data": dfa_data
    }

@app.post("/dpda/")
async def receive_dpda(dpda_data: DPDAModel):
    dpda_id = str(uuid.uuid4())
    file_path = os.path.join(DATA_DIR, f"{dpda_id}.json")
    await write_data(file_path, dpda_data.dict())
    return {
        "message": "DPDA received successfully", 
        "id": dpda_id,
        "data": dpda_data
    }

@app.get("/generate_automaton/{automaton_id}")
async def generate_automaton(automaton_id: str):
    file_path = os.path.join(DATA_DIR, f"{automaton_id}.json")
    automaton = await read_data(file_path)
    if not automaton:
        raise HTTPException(status_code=404, detail="Automaton data not found")
    draw_ntm(automaton, f"{OUTPUT_DIR}/{automaton_id}.png")
    return {"message": "Automaton image generated"}

@app.get("/automaton_image/{automaton_id}")
async def get_automaton_image(automaton_id: str):
    file_path = os.path.join(OUTPUT_DIR, f"{automaton_id}.png")
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Automaton image not found")
    return FileResponse(file_path)

class InputValidationRequest(BaseModel):
    input_str: str

async def read_data(file_path: str):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return None

@app.post("/validate_input/{automaton_id}")
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

