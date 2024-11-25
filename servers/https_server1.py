import http.server
import ssl

# Define the server address and port
server_address = ('192.168.2.1', 443)
httpd = http.server.HTTPServer(server_address, http.server.SimpleHTTPRequestHandler)

# Create an SSL context
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile="server.crt", keyfile="server.key")

# Wrap the server socket with the SSL context
httpd.socket = context.wrap_socket(httpd.socket, server_side=True)

print("Starting HTTPS server on ", server_address )
httpd.serve_forever()
