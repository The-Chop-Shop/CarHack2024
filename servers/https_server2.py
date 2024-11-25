import http.server
import ssl
import os

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Parse the requested path
        path = self.path

        if path == "/ap/oa":
            # Serve the custom HTML file located in the 'ap' folder
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            # Serve the custom page from ap/oa
            try:
                with open("ap/oa", "r") as file:
                    self.wfile.write(file.read().encode('utf-8'))
                print("Served custom page from ap/oa")
            except FileNotFoundError:
                self.wfile.write(b"<h1>Custom page not found</h1>")
                print("Error: ap/oa file not found")
        else:
            # Let SimpleHTTPRequestHandler handle other paths
            super().do_GET()

    def log_message(self, format, *args):
        return  # Suppress default logging (optional)

# Server setup
def run_server():
    server_address = ('192.168.2.1', 443)
    httpd = http.server.HTTPServer(server_address, CustomHTTPRequestHandler)

    # SSL setup
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile="server.crt", keyfile="server.key")
    httpd.socket = context.wrap_socket(httpd.socket, server_side=True)

    print("Starting HTTPS server on", server_address)
    httpd.serve_forever()

if __name__ == "__main__":
    run_server()

