# controller.py
import json
import subprocess
import os
import sys

# Config
APP_REG = '/opt/echoos/app_registry.json'
if os.name == 'nt':
    APP_REG = os.path.join(os.path.dirname(__file__), '..', 'app_registry.json')

def load_registry():
    if not os.path.exists(APP_REG):
        return {}
    try:
        with open(APP_REG, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading registry: {e}")
        return {}

def save_registry(reg):
    try:
        with open(APP_REG, 'w') as f:
            json.dump(reg, f, indent=2)
    except Exception as e:
        print(f"Error saving registry: {e}")

def open_app(app_key):
    reg = load_registry()
    if app_key not in reg:
        print(f"Error: App '{app_key}' not found in registry.")
        return False
    
    cmd = reg[app_key]['launch_cmd']
    print(f"Launching {app_key}: {cmd}")
    
    try:
        if os.name == 'nt':
            # Windows
            subprocess.Popen(cmd, shell=True)
        else:
            # Linux
            subprocess.Popen(cmd, shell=True, start_new_session=True)
        return True
    except Exception as e:
        print(f"Error launching app: {e}")
        return False

def register_app(key, path, launch_cmd):
    reg = load_registry()
    reg[key] = {'path': path, 'launch_cmd': launch_cmd}
    save_registry(reg)
    print(f"Registered '{key}' -> {launch_cmd}")

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="EchoOS App Controller")
    subparsers = parser.add_subparsers(dest='command')
    
    # Register command
    reg_parser = subparsers.add_parser('register', help='Register a new app')
    reg_parser.add_argument('key', help='App identifier (e.g., chrome)')
    reg_parser.add_argument('path', help='Path to executable')
    reg_parser.add_argument('cmd', help='Command to launch')
    
    # Open command
    open_parser = subparsers.add_parser('open', help='Open an app')
    open_parser.add_argument('key', help='App identifier')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List registered apps')

    args = parser.parse_args()
    
    if args.command == 'register':
        register_app(args.key, args.path, args.cmd)
    elif args.command == 'open':
        open_app(args.key)
    elif args.command == 'list':
        reg = load_registry()
        for k, v in reg.items():
            print(f"{k}: {v['launch_cmd']}")
    else:
        parser.print_help()
