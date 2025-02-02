from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
import json

# Load student data
with open('api/data.json', 'r') as f:
    students = json.load(f)

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Parse query parameters
        query = parse_qs(urlparse(self.path).query)
        names = query.get('name', [])
        
        # Fetch marks for requested names
        marks = []
        for name in names:
            student = next((s for s in students if s["name"] == name), None)
            marks.append(student["marks"] if student else None)
        
        # Send response
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')  # Enable CORS
        self.end_headers()
        self.wfile.write(json.dumps({"marks": marks}).encode())

# Vercel requires this named export
def app(request):
    return Handler()
