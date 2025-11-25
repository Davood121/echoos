import argparse
import os
import subprocess
import sys

def main():
    parser = argparse.ArgumentParser(description="EchoOS AI Core Launcher")
    parser.add_argument("--model", type=str, default="/opt/echoos/data/models/phi-3-mini.gguf", help="Path to GGUF model")
    parser.add_argument("--port", type=int, default=5005, help="Port to run the server on")
    parser.add_argument("--host", type=str, default="127.0.0.1", help="Host to bind to")
    args = parser.parse_args()

    if not os.path.exists(args.model):
        print(f"Error: Model file not found at {args.model}")
        print("Please download a model or update the path.")
        sys.exit(1)

    print(f"Starting AI Core with model: {args.model} on {args.host}:{args.port}")
    
    # Example using llama-cpp-python server
    # In a real scenario, you might import the server module directly or use subprocess
    cmd = [
        sys.executable, "-m", "llama_cpp.server",
        "--model", args.model,
        "--host", args.host,
        "--port", str(args.port)
    ]
    
    try:
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        print("\nStopping AI Core...")
    except Exception as e:
        print(f"Error running AI Core: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
