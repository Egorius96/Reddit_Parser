from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime
from io import BytesIO
import json


class requestHandler(BaseHTTPRequestHandler):

    file_name = 'default'
    if file_name == 'default':
        file_name: str = 'reddit-' + datetime.now().strftime('%Y%m%d') + '.txt'
    else:
        if '.' in file_name:
            if file_name.split('.')[-1] != 'txt':
                file_name = file_name.split('.')[0] + '.txt'
        else:
            file_name = file_name + '.txt'

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        if self.path == '/posts' or self.path == '/posts/':
            with open(self.file_name, 'r') as text:
                self.wfile.write(text.read().encode('utf-8'))
        elif '/posts' in self.path and not self.path.endswith('/posts/'):
            UNIQUE_ID = self.path[7:]
            with open(self.file_name, 'r') as text:
                list_strs = text.read().split('\n')
                list_dicts = []
                for dict in list_strs[:-1]:
                    list_dicts.append(eval(dict))
                for post in list_dicts:
                    if post['UNIQUE_ID'] == UNIQUE_ID:
                        self.wfile.write(str(post).encode('utf-8'))


    def do_POST(self):
        content_length = int(self.headers['Content-length'])
        body = self.rfile.read(content_length)
        response = BytesIO()
        response.write(body)
        dict_data_string = eval(str(response.getvalue())[2:-1])

        if self.path == '/posts' or self.path == '/posts/':
            with open(self.file_name, 'a+') as text:
                text.seek(0)
                file = text.read()
                count = file.count('{')
                if dict_data_string['UNIQUE_ID'] not in file:
                    self.send_response(201)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    text.write(str(dict_data_string) + ' \n')
                    self.wfile.write('{"UNIQUE_ID": "'.encode('utf-8'))
                    self.wfile.write(f'{count + 1}"'.encode('utf-8'))
                    self.wfile.write('}'.encode('utf-8'))
                else:
                    self.send_response(404)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write('Already exist!'.encode('utf-8'))

# send status

def main():
    server_address = ('', 8087)
    server = HTTPServer(server_address, requestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()
