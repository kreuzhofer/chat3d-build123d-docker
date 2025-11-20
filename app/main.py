from typing import Union
import os
import traceback

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from build123d import *

app = FastAPI()

class RenderRequest(BaseModel):
    code: str
    filename: str = "output.step"

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

@app.post("/render/")
def render_post(request: RenderRequest):
    try:
        # Execute the provided code
        exec(request.code)
        
        # Check if the specified file exists
        if os.path.exists(request.filename):
            # Return the file content in the response body
            with open(request.filename, 'rb') as f:
                file_content = f.read()
            
            # Clean up the file after reading
            os.remove(request.filename)
            
            from fastapi.responses import Response
            return Response(
                content=file_content,
                media_type="application/octet-stream",
                headers={"Content-Disposition": f"attachment; filename={request.filename}"}
            )
        else:
            raise HTTPException(status_code=400, detail="Failed to generate file")
            
    except SyntaxError as e:
        raise HTTPException(status_code=400, detail=f"Syntax error in code: {str(e)}")
    except NameError as e:
        raise HTTPException(status_code=400, detail=f"Name error in code: {str(e)}")
    except Exception as e:
        # Log the full traceback for debugging
        error_details = f"Execution error: {str(e)}\n{traceback.format_exc()}"
        raise HTTPException(status_code=500, detail=error_details)