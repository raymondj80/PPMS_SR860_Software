import socket
import threading
import time
from qdinstrument import QDInstrument


HEADER = 1024
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MSG = 'CLOSE'
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def run_server(host=SERVER, port=PORT, verbose=True):
    '''Run a QDInstrument server'''
    server = Server(host, port)
    server.start(verbose)

class Server():
    '''
    Server for connecting remotely to the IronPython console through a socket connection.
    '''
    def __init__(self, remote_host, remote_port, instrument_name="DYNACOOL"):
        self.HOST = remote_host
        self.PORT = remote_port
        self.ppms = QDInstrument(instrument_name.upper())

    def start(self, verbose):
        server.listen()
        print(f"[LISTENING] Server is listening on {SERVER}")
        while True:
            try:
                time.sleep(5)
                conn, addr = server.accept()
                thread = threading.Thread(target=self.handle_client, args=(conn, addr, verbose))
                thread.start()
                print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")
            except KeyboardInterrupt:
                break

        print(f"[CLOSING] Server disconnected.")

    def handle_client(self, conn, addr, verbose=False):
        print(f"[NEW CONNECTION] {addr} connected.")

        running = True
        while running:
            msg_length = conn.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg = conn.recv(HEADER)

                if msg.decode(FORMAT) == DISCONNECT_MSG:
                    running = False
                    print(f"[DISCONNECTING] {addr} has been disconnected.")

                else:
                    try:
                        msg = b'ppms.' + msg

                        if verbose:
                            print(f"[{addr}] {msg}")

                        if b'=' in msg:
                            exec(msg)
                            response = 'True'
                        else:
                            response = str(eval(msg))
                        conn.sendall(response.encode())
                    except (SyntaxError, NameError, AttributeError):
                        conn.sendall(b'QDInstrument Command not recognized.')
                    
        
        conn.close()

if __name__ == '__main__':
    run_server()