# filepath: /home/paulo/Documentos/REST-API-with-Automata-library/data_utils.py
import json
import os
import aiofiles
import asyncio

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