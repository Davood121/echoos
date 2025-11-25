# aurora_core/rpc_server.py
import json
import socket
import os
import threading
import subprocess

# Configuration
SOCKET_PATH = '/tmp/aurora.sock'
if os.name == 'nt':
    # On Windows, we might use a named pipe or a TCP port for simplicity in this prototype
    # Using TCP for cross-platform compatibility in this skeleton
    USE_TCP = True
    TCP_PORT = 6000
else:
    USE_TCP = False

class RPCServer:
    def __init__(self):
        self.running = True

    def handle_client(self, conn):
        try:
            while self.running:
                data = conn.recv(4096)
                if not data:
                    break
                
                try:
                    req = json.loads(data.decode('utf-8'))
                    response = self.process_request(req)
                    conn.sendall(json.dumps(response).encode('utf-8'))
                except json.JSONDecodeError:
                    err = {"error": "Invalid JSON"}
                    conn.sendall(json.dumps(err).encode('utf-8'))
        except Exception as e:
            print(f"Connection error: {e}")
        finally:
            conn.close()

    def process_request(self, req):
        method = req.get('method')
        params = req.get('params', {})
        req_id = req.get('id')
        
        print(f"RPC: {method} {params}")
        
        result = {}
        error = None
        
        if method == 'app.open':
            app_name = params.get('app')
            # In a real app, call the App Controller here
            # subprocess.run(['python', '.../controller.py', 'open', app_name])
            result = {"status": "opened", "app": app_name}
        elif method == 'system.status':
            result = {"status": "online", "battery": "100%"}
        else:
            error = "Method not found"
            
        resp = {"id": req_id}
        if error:
            resp["error"] = error
        else:
            resp["result"] = result
        return resp

    def start(self):
        if USE_TCP:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind(('127.0.0.1', TCP_PORT))
            print(f"Aurora RPC listening on TCP {TCP_PORT}")
        else:
            if os.path.exists(SOCKET_PATH):
                os.remove(SOCKET_PATH)
            s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            s.bind(SOCKET_PATH)
            print(f"Aurora RPC listening on {SOCKET_PATH}")
            
        s.listen(5)
        
        while self.running:
            conn, addr = s.accept()
            t = threading.Thread(target=self.handle_client, args=(conn,))
            t.start()

if __name__ == "__main__":
    server = RPCServer()
    try:
        server.start()
    except KeyboardInterrupt:
        print("Stopping RPC Server")
