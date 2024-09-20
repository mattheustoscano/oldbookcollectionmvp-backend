from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
from infrastructure.repositories import book_repository, user_repository
import json
import os

class RequestHandler(BaseHTTPRequestHandler):

    SWAGGER_UI_DIR = 'swagger-ui'
    SWAGGER_YAML = 'swagger.yaml'

    def _set_headers(self, status_code=200):
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers', 'Origin, Content-Type, Accept, Authorization, X-Requested-With')
        self.end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers', 'Origin, Content-Type, Accept, Authorization, X-Requested-With')
        self.end_headers()

    def do_GET(self):
        parsed_path = urlparse(self.path)
        if parsed_path.path == '/swagger':
            self.serve_static_file('index.html', self.SWAGGER_UI_DIR)
        elif parsed_path.path == '/swagger.yaml':
            self.serve_static_file(self.SWAGGER_YAML, '.')
        elif parsed_path.path == '/book/getall':
            books = book_repository.getAllBooks()
            self._set_headers()
            self.wfile.write(json.dumps(books).encode('utf-8'))
        elif parsed_path.path.startswith('/book/getbyid/'):
            try:
                id = int(parsed_path.path.split('/')[-1])
                book = book_repository.getBookById(id)
                if book:
                    self._set_headers()
                    self.wfile.write(json.dumps(book).encode('utf-8'))
                else:
                    self.send_response(404)
            except ValueError:
                self.send_response(400)
        else:
            self.send_response(404)

    def do_POST(self):
        self._set_headers()
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        data = json.loads(post_data)
        if self.path == '/book/post':
            book_repository.insertBook(data)
            self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))
        elif self.path == '/user/auth':
            user = user_repository.authenticateUser(data)
            if user:
                self.wfile.write(json.dumps(user, ensure_ascii=False).encode('utf-8'))
            else:
                self.send_response(401)
        elif self.path == '/user/post':
            user_repository.insertUser(data)
        else:
            self.send_response(404)

    def do_PUT(self):
        self._set_headers()
        if self.path.startswith('/book/put/'):
            try:
                id = int(self.path.split('/')[-1])
                content_length = int(self.headers['Content-Length'])
                put_data = self.rfile.read(content_length).decode('utf-8')
                book = json.loads(put_data)
                updated_book = book_repository.updateBook(book, id)
                self.wfile.write(json.dumps(updated_book).encode('utf-8'))
            except ValueError:
                self.send_response(400)

    def do_DELETE(self):
        self._set_headers()
        if self.path.startswith('/book/delete/'):
            try:
                id = int(self.path.split('/')[-1])
                book_repository.deleteBook(id)
                self.wfile.write(json.dumps({"message": "sucesso"}, ensure_ascii=False).encode('utf-8'))
            except ValueError:
                self.send_response(400)

    def serve_static_file(self, filename, directory):
        try:
            with open(os.path.join(directory, filename), 'rb') as file:
                self.send_response(200)
                self.send_header('Content-Type', 'text/html' if filename.endswith('.html') else 'application/octet-stream')
                self.end_headers()
                self.wfile.write(file.read())
        except IOError:
            self.send_response(404)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'File not found')

def run(server_class=HTTPServer, handler_class=RequestHandler, port=5000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd server on port {port}...')
    httpd.serve_forever()

if __name__ == "__main__":
    run()
