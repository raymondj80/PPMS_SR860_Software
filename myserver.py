import socket
from qdinstrument import QDInstrument
from time import sleep

from server_params import _HOST, _PORT

def run_server(host=_HOST, port=_PORT, verbose=True):
    '''Run a QDInstrument server'''
    server = Server(host, port)
    server.run(verbose)

class Server():
    '''
    Server for connecting remotely to the IronPython console through a socket connection.
    '''
    def __init__(self, remote_host, remote_port, instrument_name="DYNACOOL"):
        self.HOST = remote_host
        self.PORT = remote_port
        self.ppms = QDInstrument(instrument_name.upper())

    def run(self, verbose=False):
        '''Run a measurement server for remote communication.'''
        
        ppms = self.ppms
        print('Creating socket at %s:%s...' %(self.HOST, self.PORT))
        
        keep_running =True
        while keep_running:
            
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((self.HOST, self.PORT))
            s.listen(1)
            conn, addr = s.accept()
            print('Connected by', addr)
            while keep_running:
                cmd = conn.recv(1024)
                print(cmd.decode())
                if not cmd: break
                
                if cmd.decode() == 'EXIT':
                    conn.send(bytes('Server exiting.', 'utf-8'))
                    print('Server exiting.')
                    sleep(0.1)
                    keep_running = False
                elif cmd.decode() == 'CLOSE':
                    conn.send(b'Closing connection.')
                    print('Client ({0}, {1}) disconnected.'.format(self.HOST, self.PORT))
                    sleep(0.1)
                    conn.close()
                    # s.close()
                    keep_running = False
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
            
            
            conn.close()
            


if __name__ == '__main__':
    run_server()