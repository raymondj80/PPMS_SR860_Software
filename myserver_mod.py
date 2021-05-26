import socket
from qdinstrument import QDInstrument
from time import sleep

HEADER = 1024
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MSG = "!DISCONNECT"
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
            conn, addr = server.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr, verbose))
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

    def handle_client(self, conn, addr, verbose=False):
        print(f"[NEW CONNECTION] {addr} connected.")

        running = True
        while running:
            msg_length = conn.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg = conn.recv(msg_length).decode(FORMAT)

                if msg == DISCONNECT_MSG:
                    running = False
                    print(f"[DISCONNECTING] {addr} has been disconnected.")

                else:

                    print(f"[{addr}] {msg}")
        
        conn.close()
    

    def run(self, verbose=False):
        '''Run a measurement server for remote communication.'''
        
        ppms = self.ppms
        print('Creating socket at %s:%s...' %(self.HOST, self.PORT))
        
        keep_running =True
        keep_running_socket = True
        while keep_running:
            
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((self.HOST, self.PORT))
            s.listen(1)
            #conn, addr = s.accept() (moved by Spencer into while loop 5/19/21)
            #print('Connected by', addr)
            while keep_running_socket:
                conn, addr = s.accept()
                print('Connected by', addr)
                cmd = conn.recv(1024)
                print(cmd.decode())
                if not cmd: break
        
                if cmd.decode() == 'EXIT':
                    conn.send(bytes('Server exiting.', 'utf-8'))
                    print('Server exiting.')
                    sleep(0.1)
                    keep_running_socket = False
                    keep_running = False
                elif cmd.decode() == 'CLOSE':
                    conn.send(b'Closing connection.')
                    #print('Client ({0}, {1}) disconnected.'.format(self.HOST, self.PORT))
                    print('Client {0} disconnected.'.format(addr))
                    sleep(0.1)
                    conn.close()
                    # s.close()
                    keep_running_socket = True #changed from False by Spencer 5/19/21
                else:
                    try:
                        cmd = b'ppms.' + cmd
                        if verbose: print(cmd.decode())
                        if b'=' in cmd:
                            exec(cmd)
                            response = 'True'
                        else:
                            response = str(eval(cmd))
                        conn.sendall(response.encode())
                    except (SyntaxError, NameError, AttributeError):
                        conn.sendall(b'QDInstrument Command not recognized.')
            
            
            #conn.close() (commented out by Spencer 5/19/21)
            


if __name__ == '__main__':
    run_server()