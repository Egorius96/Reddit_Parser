import hashlib
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from io import BytesIO


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
        self.send_response(201)
        self.end_headers()
        try:
            if self.path == '/posts' or self.path == '/posts/':
                with open(self.file_name, 'r') as text:
                    self.wfile.write(text.read().encode('utf-8'))

            elif '/posts' in self.path and not self.path.endswith('/posts/'):
                UNIQUE_ID = self.path[7:]
                with open(self.file_name, 'r') as text:
                    list_dicts = eval(text.read())
                    for post in list_dicts:
                        if post['UNIQUE_ID'] == UNIQUE_ID:
                            self.wfile.write(str(post).encode('utf-8'))
        except FileNotFoundError:
            self.wfile.write('File does not exist'.encode('utf-8'))



    def do_POST(self):
        content_length = int(self.headers['Content-length'])
        body = self.rfile.read(content_length)
        response = BytesIO()
        response.write(body)
        dict_data_string = eval(str(response.getvalue())[2:-1])
        replacing_content = []
        if self.path == '/posts' or self.path == '/posts/':
            try:
                with open(self.file_name, 'r') as text:
                    replacing_content = text.read()
            except FileNotFoundError:
                print('File does not exist')

            if replacing_content == '':
                del replacing_content
                replacing_content = []

            if dict_data_string['UNIQUE_ID'] not in replacing_content:
                if len(replacing_content) != 0:
                    replacing_content = eval(replacing_content)
                replacing_content.append(dict_data_string)
                with open(self.file_name, 'w') as text:
                        self.send_response(201)
                        self.send_header('Content-type', 'application/json')
                        self.end_headers()
                        text.write(str(replacing_content))
                        self.wfile.write('{"UNIQUE_ID": "'.encode('utf-8'))
                        self.wfile.write(f'{len(replacing_content)}]"'.encode('utf-8'))
                        self.wfile.write('}'.encode('utf-8'))
            else:
                self.send_response(404)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write('Already exist!'.encode('utf-8'))


    def do_DELETE(self):
        UNIQUE_ID = self.path[1:]
        replacing_content = []
        with open(self.file_name, 'r') as text:
            hash1 = hashlib.md5(text.read().encode('utf-8')).hexdigest()
        with open(self.file_name, 'r') as text:
            list_dicts = eval(text.read())
        for line in list_dicts:
            if UNIQUE_ID != line['UNIQUE_ID']:
                replacing_content.append(line)
        del line
        with open(self.file_name, 'w') as text:
            text.write(str(replacing_content))
        with open(self.file_name, 'r') as text:
            hash2 = hashlib.md5(text.read().encode('utf-8')).hexdigest()
        if hash1 == hash2:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(f'Line with UNIQUE_ID = {UNIQUE_ID} not found'.encode('utf-8'))
        else:
            self.send_response(201)
            self.end_headers()
            self.wfile.write('Deletion completed!'.encode('utf-8'))


    def do_PUT(self):
        UNIQUE_ID = self.path[1:]
        replacing_content = []
        content_length = int(self.headers['Content-length'])
        body = self.rfile.read(content_length)
        response = BytesIO()
        response.write(body)
        dict_data_string = eval(str(response.getvalue())[2:-1])
        with open(self.file_name, 'r') as text:
            hash1 = hashlib.md5(text.read().encode('utf-8')).hexdigest()

        with open(self.file_name, 'r') as text:
            list_dicts = eval(text.read())
        for line in list_dicts:
            if UNIQUE_ID != line['UNIQUE_ID']:
                replacing_content.append(line)
            else:
                replacing_content.append(dict_data_string)
        del line
        with open(self.file_name, 'w') as text:
            text.write(str(replacing_content))
        with open(self.file_name, 'r') as text:
            hash2 = hashlib.md5(text.read().encode('utf-8')).hexdigest()
        if hash1 == hash2:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(f'Line with UNIQUE_ID = {UNIQUE_ID}'
                             f' not found or there were no changes'.encode('utf-8'))
        else:
            self.send_response(201)
            self.end_headers()
            self.wfile.write('Replacement completed!'.encode('utf-8'))


def main():
    server_address = ('', 8087)
    server = HTTPServer(server_address, requestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()
