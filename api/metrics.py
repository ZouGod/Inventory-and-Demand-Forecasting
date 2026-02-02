from http.server import BaseHTTPRequestHandler
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from api.models_handler import ModelHandler
    model_handler = ModelHandler()
except Exception as e:
    model_handler = None
    print(f"Error loading model: {e}")

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if model_handler is None:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = json.dumps({'error': 'Model not loaded'})
                self.wfile.write(response.encode())
                return
            
            model_metrics = model_handler.get_metrics()
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = json.dumps(model_metrics)
            self.wfile.write(response.encode())
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = json.dumps({'error': str(e)})
            self.wfile.write(response.encode())
