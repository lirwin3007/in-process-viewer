import os
import http.server
import socketserver

# Check for updates
# TODO

# Determine the port number
if 'IN_PROCESS_PORT' in os.environ:
  PORT = os.environ['IN_PROCESS_PORT']
  print("IN_PROCESS_PORT found:", PORT)
else:
  PORT = 8000
  print("IN_PROCESS_PORT not found. Using port", PORT)

# Define the request handler
class ClientRequestHandler(http.server.SimpleHTTPRequestHandler):
  def do_GET(self):
    self.path = f"client{self.path}"
    return http.server.SimpleHTTPRequestHandler.do_GET(self)

# Instantiate the request handler
Handler = ClientRequestHandler

# Begin the webserver
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("Serving at port", PORT)
    httpd.serve_forever()
