import subprocess
import shlex

WHITELIST = ['uptime', 'ls', 'df', 'whoami', 'date', 'echo']

def safe_run(cmd_str):
    """
    Runs a command if it's in the whitelist.
    """
    try:
        # Basic parsing
        parts = shlex.split(cmd_str)
        if not parts:
            return "Error: Empty command"
            
        base = parts[0]
        if base not in WHITELIST:
            raise PermissionError(f"Command '{base}' is not allowed")
            
        # Run the command
        result = subprocess.run(parts, capture_output=True, text=True, timeout=5)
        
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            return f"Error ({result.returncode}): {result.stderr.strip()}"
            
    except Exception as e:
        return f"Execution failed: {e}"

if __name__ == "__main__":
    # Simple test
    print("Testing safe_run...")
    print(f"ls: {safe_run('ls -la')}")
    print(f"whoami: {safe_run('whoami')}")
    try:
        print(f"rm: {safe_run('rm -rf /')}")
    except Exception as e:
        print(f"Blocked rm: {e}")
