import socket
import time
import threading
from rockcomm.commsocket import CommSocket
from rockcomm.datasave import Data
from rockcomm.connexionthread import ConnexionThread


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

class CommandAnswerSocket(CommSocket):
    def comm(self):
        command = self.sock.recv(2048)
        if command == b'SEND HELLO':
            self.sock.send(b'Hello')
        self.sock.close()


class DatasendThread(threading.Thread):
    def __init__(self, address, data, continuous=True):
        threading.Thread.__init__(self)
        self.address = address
        self.data = data
        self.continuous = continuous
        return

    def run(self):
        while(self.continuous):
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect(self.address)
            DSendSock = DatasendSocket(self.sock)
            DSendSock.sendData(self.data)
            self.sock.close()
            time.sleep(1)
        print('Datasend Thread at {} shutting down'.format(self.address))