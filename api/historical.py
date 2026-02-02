from http.server import BaseHTTPRequestHandler
import json
import os
import sys
from urllib.parse import urlparse, parse_qs

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from api.data_processor import DataProcessor
    data_processor = DataProcessor()
except Exception as e:
    data_processor = None
    print(f"Error loading data processor: {e}")

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            query_params = parse_qs(urlparse(self.path).query)
            product_id = query_params.get('product_id', [None])[0]
            
            if not product_id:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = json.dumps({'error': 'product_id is required'})
                self.wfile.write(response.encode())
                return
            
            if data_processor is None:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = json.dumps({'error': 'Data processor not loaded'})
                self.wfile.write(response.encode())
                return
            
            historical_data = data_processor.get_historical(product_id)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = json.dumps({'data': historical_data})
            self.wfile.write(response.encode())
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = json.dumps({'error': str(e)})
            self.wfile.write(response.encode())
