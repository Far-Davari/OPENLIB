import http.server
import socketserver
import os

PORT = 8000

os.chdir("docs")

Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"The Server Runs Over port {PORT}. http://localhost:{PORT}")
    httpd.serve_forever()
