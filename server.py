import hashlib
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from io import BytesIO
import logging


class RequestHandler(BaseHTTPRequestHandler):
    """
    A class that includes a set of functions for processing requests (GET, POST, DELETE, PUT)
    """

    ''' Setting the name for the output file '''
    file_name = 'default'
    if file_name == 'default':
        file_name: str = 'reddit-' + datetime.now().strftime('%Y%m%d') + '.txt'
    else:
        if '.' in file_name:
            if file_name.split('.')[-1] != 'txt':
                file_name = file_name.split('.')[0] + '.txt'
        else:
            file_name = file_name + '.txt'

    def do_GET(self) -> None:
        """
        Triggered when a GET request is received, checks the contents of self.path
        and based on this sends a response with the contents of the file
        """
        try:
            '''sending a response with all the contents of the file'''
            if self.path == '/posts' or self.path == '/posts/':
                with open(self.file_name, 'r') as text:
                    self.send_response(201)
                    self.end_headers()
                    self.wfile.write(text.read().encode('utf-8'))

                ''' sending a response with data by UNIQUE_ID
                if the UNIQUE_ID exists, the response code is 201
                if the UNIQUE_ID does not exist, the response code is 404 '''
            elif '/posts' in self.path and not self.path.endswith('/posts/'):
                UNIQUE_ID = self.path.split('/')[2]
                with open(self.file_name, 'r') as text:
                    list_dicts = eval(text.read())
                    for post in list_dicts:
                        if post['UNIQUE_ID'] == UNIQUE_ID:
                            self.send_response(201)
                            self.end_headers()
                            self.wfile.write(str(post).encode('utf-8'))
                    else:
                        self.send_response(404)
                        self.end_headers()
                        self.wfile.write(f'Line with UNIQUE_ID = {UNIQUE_ID} not found'.encode('utf-8'))
        except FileNotFoundError:
            self.send_response(404)
            self.end_headers()
            self.wfile.write('File does not exist'.encode('utf-8'))

    def do_POST(self) -> None:
        """
        Triggered when a POST request is received, processes incoming data, saves it to a file
        """
        content_length = int(self.headers['Content-length'])
        body = self.rfile.read(content_length)
        response = BytesIO()
        response.write(body)
        dict_data_string = eval(str(response.getvalue())[2:-1])
        replacing_content = []
        if self.path == '/posts' or self.path == '/posts/':
            try:
                ''' Checks if the file exists, saves the contents of the file '''
                with open(self.file_name, 'r') as text:
                    replacing_content = text.read()
            except FileNotFoundError:
                print('File does not exist')
                logging.basicConfig(filename='serverlog-' + datetime.now().strftime('%Y%m%d')
                                             + '.txt', level=logging.WARNING)
                logging.warning(f'{FileNotFoundError} - File does not exist')

            ''' Check if the file is created, but empty, then replacing_content var
            will be in string format (dictionary is needed).'''
            if replacing_content == '':
                del replacing_content
                replacing_content = []

            '''checking the existing UNIQUE_ID in the file
            if the UNIQUE_ID exists, the response code is 201
            if the UNIQUE_ID does not exist, the response code is 404'''
            if dict_data_string['UNIQUE_ID'] not in replacing_content:

                '''if the file is not empty, it forms a dictionary file type
                for the convenience of further work on the data.'''
                if len(replacing_content) != 0:
                    replacing_content = eval(replacing_content)

                '''adding new data to var'''
                replacing_content.append(dict_data_string)

                '''writing new content to a file'''
                with open(self.file_name, 'w') as text:
                        self.send_response(201)
                        self.send_header('Content-type', 'application/json')
                        self.end_headers()
                        text.write(str(replacing_content))
                        self.wfile.write('{"UNIQUE_ID": "'.encode('utf-8'))
                        self.wfile.write(f'{len(replacing_content)}]"'.encode('utf-8'))
                        self.wfile.write('}'.encode('utf-8'))

                '''if the UNIQUE_ID does not exist, the response code is 404'''
            else:
                self.send_response(404)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write('Already exist!'.encode('utf-8'))

    def do_DELETE(self) -> None:
        """
        Triggered when a DELETE request is received, checks for records containing
        the passed UNIQUE_ID. If successful, deletes the data. If the UNIQUE_ID does not exist,
        it sends a 404 response.
        Verification is performed by comparing the hash sum of the file before
        deletion and the hash sum of the file after deletion.
        """
        UNIQUE_ID = self.path.split('/')[1]
        replacing_content = []

        '''saving the hash sum before the change'''
        with open(self.file_name, 'r') as text:
            old_hash = hashlib.md5(text.read().encode('utf-8')).hexdigest()

        '''writing file contents to var'''
        with open(self.file_name, 'r') as text:
            list_dicts = eval(text.read())

        '''checking the existing UNIQUE_ID in the file'''
        for line in list_dicts:
            if UNIQUE_ID != line['UNIQUE_ID']:
                replacing_content.append(line)

        '''writing modified data to a file'''
        with open(self.file_name, 'w') as text:
            text.write(str(replacing_content))

        '''saving the hash sum after the change'''
        with open(self.file_name, 'r') as text:
            new_hash = hashlib.md5(text.read().encode('utf-8')).hexdigest()

        '''hash sum comparison and sending a response'''
        if old_hash == new_hash:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(f'Line with UNIQUE_ID = {UNIQUE_ID} not found'.encode('utf-8'))
        else:
            self.send_response(201)
            self.end_headers()
            self.wfile.write('Deletion completed!'.encode('utf-8'))

    def do_PUT(self) -> None:
        """
        Triggered when a PUT request is received, checks for records containing
        the passed UNIQUE_ID. If successful, it makes changes to the data.
        If the UNIQUE_ID does not exist, it sends a 404 response.
        Verification is performed by comparing the hash sum of the file before
        changing data and the hash sum of the file after changing data.
        """
        UNIQUE_ID = self.path.split('/')[1]
        replacing_content = []
        content_length = int(self.headers['Content-length'])
        body = self.rfile.read(content_length)
        response = BytesIO()
        response.write(body)
        dict_data_string = eval(str(response.getvalue())[2:-1])

        '''saving the hash sum before the change'''
        with open(self.file_name, 'r') as text:
            old_hash = hashlib.md5(text.read().encode('utf-8')).hexdigest()

        '''writing file contents to var'''
        with open(self.file_name, 'r') as text:
            list_dicts = eval(text.read())

        '''checking the existing UNIQUE_ID in the file'''
        for line in list_dicts:
            if UNIQUE_ID != line['UNIQUE_ID']:
                replacing_content.append(line)
            else:
                replacing_content.append(dict_data_string)

        '''writing modified data to a file'''
        with open(self.file_name, 'w') as text:
            text.write(str(replacing_content))

        '''saving the hash sum after the change'''
        with open(self.file_name, 'r') as text:
            new_hash = hashlib.md5(text.read().encode('utf-8')).hexdigest()

        '''hash sum comparison and sending a response'''
        if old_hash == new_hash:
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
    server = HTTPServer(server_address, RequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()
