import socket
import time


class DatasendSocket():
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def sendData(self, data):
        #print('sending')
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.ip,self.port))
        self.sock.send(data.dtype.encode())
        check = self.sock.recv(2048)
        if check != b'DTYPE RCVED':
            raise RuntimeError('Problem with dtype sending : {}'.format(check))
        #print('dtype sent')
        self.sock.send(str(data.dvalue).encode())
        check = self.sock.recv(2048)
        if check != b'DVALUE RCVED':
            raise RuntimeError('Problem with dtype sending : {}'.format(check))
        #print('dvalue sent')
        self.sock.send('EOD'.encode())
        check = self.sock.recv(2048)
        if check != b'EOD RCVED':
            raise RuntimeError('Problem with EOD sending : {}'.format(check.decode()))
        self.sock.close()
