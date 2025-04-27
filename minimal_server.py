from http.server import BaseHTTPRequestHandler, HTTPServer
import json

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def _set_headers(self, content_type="application/json"):
        self.send_response(200)
        self.send_header('Content-type', content_type)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_OPTIONS(self):
        self._set_headers()
        
    def do_GET(self):
        self._set_headers()
        response = {
            "message": "Jen Lango Backend is running!"
        }
        self.wfile.write(json.dumps(response).encode())
        
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode('utf-8'))
            message = data.get('message', '')
            
            # Simple Hindi responses
            if message == "आप कैसे हो":
                response = {
                    "text": "मैं बहुत अच्छा हूँ, धन्यवाद! आप कैसे हैं?",
                    "audio_url": "",
                    "feedback": {
                        "proficiency": "Intermediate",
                        "pronunciation": "Good",
                        "cultural_context": "This is a common greeting in Hindi"
                    }
                }
            else:
                response = {
                    "text": f"You said: {message}",
                    "audio_url": "",
                    "feedback": {
                        "proficiency": "Beginner",
                        "pronunciation": "Needs practice",
                        "cultural_context": "Try using more Hindi phrases"
                    }
                }
                
            self._set_headers()
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            self._set_headers()
            error_response = {"error": str(e)}
            self.wfile.write(json.dumps(error_response).encode())

def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting server on port {port}...")
    httpd.serve_forever()

if __name__ == "__main__":
    run(port=8000)
