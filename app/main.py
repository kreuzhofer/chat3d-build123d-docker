from typing import Union
import os

from fastapi import FastAPI
from fastapi.responses import FileResponse
from build123d import *

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World 4"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.get("/render/")
def render():
    try:
        # Code block to execute as eval from string
        code_to_execute = """
with BuildPart() as box_builder:
    Box(10, 10, 10)
    export_step(box_builder.part, "box.step")
"""
        
        # Execute the code block
        exec(code_to_execute)
        
        if os.path.exists("box.step"):
            return FileResponse("box.step", media_type="application/octet-stream", filename="box.step")
        else:
            return {"status": "error", "message": "Failed to generate file"}
    except Exception as e:
        return {"status": "error", "message": str(e)}