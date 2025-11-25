import argparse
import os
import subprocess
import sys
import time
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

# Try importing ollama
try:
    import ollama
except ImportError:
    print("Error: 'ollama' python package not found. Please run: pip install ollama")
    sys.exit(1)

MODEL_NAME = "phi3:3.8b"

app = FastAPI()

class ChatRequest(BaseModel):
    message: str
    history: list = []

@app.post("/chat")
async def chat(req: ChatRequest):
    """
    Chat endpoint that forwards to Ollama.
    """
    try:
        # Construct messages with system prompt
        messages = [{'role': 'system', 'content': 'You are EchoOS, an advanced AI assistant operating system. You control the computer and help the user.'}]
        
        # Add history (simplified)
        for msg in req.history:
            messages.append(msg)
            
        messages.append({'role': 'user', 'content': req.message})
        
        response = ollama.chat(model=MODEL_NAME, messages=messages)
        return {"response": response['message']['content']}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def ensure_model():
    """
    Checks if the model exists, pulls it if not.
    """
    print(f"Checking for model: {MODEL_NAME}...")
    try:
        # List models
        models = ollama.list()
        # Check if model is in the list (handling different response formats)
        found = False
        if 'models' in models:
            for m in models['models']:
                if MODEL_NAME in m['name']:
                    found = True
                    break
        
        if not found:
            print(f"Model {MODEL_NAME} not found. Pulling (this may take a while)...")
            ollama.pull(MODEL_NAME)
            print("Model pulled successfully!")
        else:
            print(f"Model {MODEL_NAME} is ready.")
            
    except Exception as e:
        print(f"Error checking/pulling model: {e}")
        print("Make sure Ollama is running (run 'ollama serve' in a separate terminal if needed).")

def main():
    parser = argparse.ArgumentParser(description="EchoOS AI Core (Ollama)")
    parser.add_argument("--port", type=int, default=5005, help="Port to run the API on")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Host to bind to")
    args = parser.parse_args()

    # Ensure Ollama is ready
    ensure_model()

    print(f"Starting EchoOS AI Core on {args.host}:{args.port}")
    uvicorn.run(app, host=args.host, port=args.port)

if __name__ == "__main__":
    main()
