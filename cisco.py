from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import signal
import sys
import time

url_blacklist = {
    "theteflacademy.co.uk": "This URL is known to contain malware.",
    "ali213.net": "This URL might contain adware."
}

# Throttling parameters, 5 requests max per second, token resets every second
MAX_REQUESTS_PER_SECOND = 5
TOKEN_REFRESH_INTERVAL = 1.0 / MAX_REQUESTS_PER_SECOND
tokens = MAX_REQUESTS_PER_SECOND
last_refresh_time = time.time()

class MaliciousURLLookup(BaseHTTPRequestHandler):
    def do_GET(self):
        global tokens, last_refresh_time
        
        # Throttle requests
        current_time = time.time()
        elapsed_time = current_time - last_refresh_time
        tokens = min(tokens + elapsed_time * MAX_REQUESTS_PER_SECOND, MAX_REQUESTS_PER_SECOND)
        last_refresh_time = current_time
        
        if tokens < 1:
            self.send_error(429, 'Too Many Requests per second !')
            self.end_headers()
            return
        
        tokens -= 1 
        
        if self.path.startswith('/v1/urlinfo/'):
            # Extract the URL from the request path by stripping
            url = self.path[len('/v1/urlinfo/'):]
            url = url.strip('/')

            # Check if the URL is known to contain malware
            if url in url_blacklist:
                
                # If found, return a response indicating that the URL is not safe
                response = {
                    "url": url,
                    "safe": False,
                    "message": url_blacklist[url]
                }
            else:
                # If not found, return a response indicating that the URL not in the blacklist and is safe
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
    server_address = ('', 8080) # Make sure your por 8080 is available, http://localhost:8080/v1/urlinfo/
    httpd = server_class(server_address, handler_class)

    # Handle Ctrl+C interrupt signal  
    def signal_handler(sig, frame):
        print('Shutting down server...')
        httpd.server_close()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    
    print('Application is running...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()