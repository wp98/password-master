import socket
from threading import Thread, activeCount

import Database

"""
REQUESTS:
L - LOGIN, R - REGISTER, A - ADD PASS, D - DELETE PASS, S - SHOW PASS
Q - DISCONNECT
"""

HEADER = 256
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'


class Server:
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(ADDR)
        self.database = Database.Database()

    def handle_client(self, conn, addr):
        print(f'[NEW CONNECTION] {addr} CONNECTED')
        connected = True
        while connected:
            client_request = conn.recv(HEADER).decode(FORMAT)
            if client_request:
                client_request = client_request.split(';')
                if client_request[0] == 'L':
                    login_request = """SELECT user_name, password FROM users WHERE user_name='{}'""".format(
                        client_request[1])
                    login_result = self.database.send_query(login_request)
                    if client_request:
                        if client_request[1] == login_result[0][0] and client_request[2] == login_result[0][1]:
                            self.send_response('1', conn)
                        else:
                            self.send_response('0', conn)
                if client_request[0] == 'R':
                    register_results = self.database.add_user(client_request[1], client_request[2])
                    if register_results:
                        self.send_response('1', conn)
                    else:
                        self.send_response(str(register_results), conn)
                if client_request[0] == 'A':
                    add_pass_result = self.database.insert_pass(client_request[1], client_request[2], client_request[3])
                    if add_pass_result:
                        self.send_response('1', conn)
                    else:
                        self.send_response('0', conn)
                if client_request[0] == 'D':
                    delete_result = self.database.delete_pass(client_request[1], client_request[2])
                    if delete_result:
                        self.send_response('1', conn)
                    else:
                        self.send_response('0', conn)
                if client_request[0] == 'S':
                    show_request = """SELECT * FROM {}""".format(client_request[1])
                    pass_list = self.database.send_query(show_request)
                    if pass_list:
                        conn.send(self.list_encode(pass_list))
                    else:
                        self.send_response('Empty', conn)
                if client_request[0] == 'Q':
                    connected = False
        print(f'[DISCONNECT] {addr}')
        conn.close()

    def start_server(self):
        self.server.listen()
        print(f'[LISTENING] LISTENING ON {SERVER}')
        while True:
            conn, addr = self.server.accept()
            thread = Thread(target=self.handle_client, args=(conn, addr))
            thread.start()
            print(f'[ACTIVE CONNECTIONS] {activeCount() - 1}')

    def send_response(self, response, conn):
        conn.send(response.encode(FORMAT))

    def list_encode(self, data):
        stream_string = ''
        for col in data:
            for row in col:
                stream_string += str(row) + ';'
        return stream_string.encode(FORMAT)


print(f'[STARTING] SERVER IS STARTING...')
server = Server()
server.start_server()
