from http.server import HTTPServer, BaseHTTPRequestHandler

IP = ''
PORT = 1476

class App(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/ui.html'
        if self.path == '/ui.html' or self.path == '/script.js':
            content_type = 'text/html' if self.path == '/ui.html' else 'text/javascript'
            self.send_response(200)
            self.send_header('Content-type', content_type)
            self.end_headers()

            with open(self.path[1:], 'rb') as file:
                self.wfile.write(file.read())
        else:
            self.send_response(404)
            self.end_headers()


if __name__ == '__main__':
    server_address = (IP, PORT)
    httpd = HTTPServer(server_address, App)
    print(f"Server running at {IP}:{PORT}")
    httpd.serve_forever()
