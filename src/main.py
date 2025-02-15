from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse
import os
import json
from typing import Optional
import uvicorn
from datetime import datetime
import subprocess
import sqlite3
from pathlib import Path
import shutil
from openai import OpenAI

app = FastAPI()

# Initialize OpenAI client
client = OpenAI(api_key=os.environ.get("AIPROXY_TOKEN"))

def ensure_data_directory():
    """Ensure the /data directory exists"""
    os.makedirs("/data", exist_ok=True)

def is_path_safe(path: str) -> bool:
    """Check if the path is within /data directory"""
    try:
        resolved_path = os.path.realpath(path)
        return resolved_path.startswith("/data")
    except:
        return False

@app.post("/run")
async def run_task(task: str):
    try:
        # Parse task using LLM
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a task parser. Analyze the given task and identify the operation type and required parameters."},
                {"role": "user", "content": task}
            ]
        )
        
        parsed_task = response.choices[0].message.content
        task_type = json.loads(parsed_task).get("type")
        
        # Execute task based on type
        if task_type == "format_markdown":
            # Implementation for A2
            pass
        elif task_type == "count_weekdays":
            # Implementation for A3
            pass
        # Add other task implementations
        
        return {"status": "success", "message": "Task completed successfully"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/read")
async def read_file(path: str):
    if not is_path_safe(path):
        raise HTTPException(status_code=400, detail="Invalid path")
    
    try:
        with open(path, 'r') as file:
            content = file.read()
        return PlainTextResponse(content)
    except FileNotFoundError:
        raise HTTPException(status_code=404)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    ensure_data_directory()
    uvicorn.run(app, host="0.0.0.0", port=8000)