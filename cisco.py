from http.server import BaseHTTPRequestHandler, HTTPServer
import json

urls_lookuptable = {
    "theteflacademy.co.uk": "This URL is known to contain malware.",
    "google.com": "This URL is safe to access."
}

class MaliciousURLLookup(BaseHTTPRequestHandler):
    def do_GET(self):
        
        if self.path.startswith('/v1/urlinfo/'):
            # Extract the URL from the request path by stripping
            url = self.path[len('/v1/urlinfo/'):]
            url = url.strip('/')

            # Check if the URL is known to contain malware
            if url in urls_lookuptable:
                
                # If found, return a response indicating that the URL is not safe
                response = {
                    "url": url,
                    "safe": False,
                    "message": urls_lookuptable[url]
                }
            else:
                # If not found, return a response indicating that the URL is safe
                response = {
                    "url": url,
                    "safe": True,
                    "message": "The URL entered is not in the blacklist"
                }

            # Contruct response
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))

def run(server_class=HTTPServer, handler_class=MaliciousURLLookup):
    print('Starting application...')
    server_address = ('', 8080) # Make sure your por 8080 is available
    httpd = server_class(server_address, handler_class)
    
    print('Application is running...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()