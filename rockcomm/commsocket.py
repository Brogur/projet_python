#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 15:48:10 2019

@author: alseidon
"""

import socket
import time
from .datasave import Data

class CommSocket():
    """
    Motherclass of socket designed to send or receive one instance.
    """
    def __init__(self, sock, address):
        """
        

        Parameters
        ----------
        sock : socket.socket
            socket to upgrade.
        address : (host, port)
            IP address (host, port)= assigned to the socket.

        Returns
        -------
        None.

        """
        self.sock = sock
        self.address = address

    
    def sendChecked(self, msg, maxtrys=10): #MUST rethink recv accordingly
        """
        Improved version of socket.send : verifies length of received message and tries again if needed.
        
        Parameters
        ----------
        msg : bytes (binary str)
            message to send.
        maxtrys : int, optional
            maximum send trys. The default is 10.
        
        Returns
        -------
        None.
        """
        checkBytes, attempts = 0, 0
        L = len(msg)
        while checkBytes != L:
            checkBytes = self.sock.send(msg)
            attempts += 1
            if attempts > maxtrys:
                raise RuntimeError('{} couldn\'t be sent in {} attempts'.format(msg, attempts))
        return attempts
    
    def defsend(self, sendChecked):
        if sendChecked:
            self.send = self.sendChecked
        else:
            self.send = self.sock.send
    
    def comm(self, sendChecked=False):
        """
        Method defined for each daughter class. Communicates to send or receive the instance.

        Parameters
        ----------
        sendChecked: bool, optional.
            whether to use the modified send method or not. The default is False.
        
        Returns
        -------
        None.

        """
        pass



class DatarcvSocket(CommSocket):
    """
    Socket to receive one data
    """
    def comm(self, sendChecked=False):
        """
        Receives one data at (self.ip, self.port).
        Format : receives the data type, then data value, then sends EOD (end of data) ; then deconnects.
        
        Parameters
        ----------
        sendChecked: bool, optional.
            whether to use the modified send method or not. The default is False.
        
        Returns
        -------
        Data
            Instance of Data, with dtype, dvalue and time of reception.

        """
        errorgotten = False
        #print("Connexion de {}" % (self.address))
        self.defsend(sendChecked)

        dtype = self.sock.recv(2048).decode()
        self.send(b'DTYPE RCVED')
        dvalue = self.sock.recv(2048).decode()
        self.send(b'DVALUE RCVED')
        EndMsg = self.sock.recv(2048)
        if EndMsg != b'EOD':
            print(EndMsg.decode())
            self.send(b'Error: EOD not received')
            errorgotten = True
        else:
            self.send(b'EOD RCVED')

        self.sock.close()
        if not errorgotten:
            return Data(dtype, dvalue, time.time()) #at this point we consider time of measure and time of rcv are similar
        return Data('Error', 0, time.time())



class CommandSocket(CommSocket):
    """
    Socket to send one command to the machine.
    """
    def __init__(self, sock, address, msg=b''):
        """
        

        Parameters
        ----------
        sock : socket.socket
            socket to upgrade.
        address : (host, port)
            IP address (host, port)= assigned to the socket.
        msg : bytes (binary str), optional
            command to send. The default is b''.

        Returns
        -------
        None.

        """
        CommSocket.__init__(self, sock, address)
        self.msg = msg

    def comm(self, sendChecked=False):
        """
        Sends the command.

        Parameters
        ----------
        sendChecked: bool, optional.
            whether to use the modified send method or not. The default is False.

        Returns
        -------
        answer: bytes (binary str)
            answer given by the machine.

        """
        self.defsend(sendChecked)
        #print("Connexion de %s %s" % (self.ip, self.port, ))
        self.send(self.msg.encode())
        answer = self.sock.recv(2048)
        self.sock.close()
        return answer



class UserSocket(CommSocket):
    """
    Socket to receive commands from the user and answer them.
    """
    def comm_command(self, sendChecked=False):
        """
        receives one command from the user.

        Parameters
        ----------
        sendChecked: bool, optional.
            whether to use the modified send method or not. The default is False.

        Returns
        -------
        command : bytes (binary str)
            command received.

        """
        self.defsend(sendChecked)
        command = self.sock.recv(2048)
        self.send(b'command received')
        return command

    def comm_answer(self, answer, sendChecked=False):
        """
        sends answer to the user.

        Parameters
        ----------
        answer : bytes (binary str)
            answer to send.
        sendChecked: bool, optional.
            whether to use the modified send method or not. The default is False.

        Raises
        ------
        Exception
            If answer hasn't been correctly received.

        Returns
        -------
        None.

        """
        self.defsend(sendChecked)
        self.send(answer)
        confirmation = self.sock.recv(2048)
        self.sock.close()
        if confirmation != b'answer rcved':
            raise Exception('Answer incorrectly received: {}'.format(confirmation))
        return



class InfoSocket(CommSocket):
    """
    Socket to send automatic infos to the user.
    """
    def __init__(self, sock, address, info):
        CommSocket.__init__(self, sock, address)
        self.info = info
        return
    
    def comm(self, sendChecked=False):
        """
        sends one information (str) to the user.

        Parameters
        ----------
        sendChecked: bool, optional.
            whether to use the modified send method or not. The default is False.

        Returns
        -------
        None.

        """
        self.defsend(sendChecked)
        self.send(self.info.encode())
        confirmation = self.sock.recv(2048)
        if confirmation != b'info rcved':
            raise Exception('Problem with info sending: {}'.format(confirmation))
        self.sock.close()
        return



def bindsocket(port, host=''):
    """
    Creates a socket assigned to the IP address (host, port).

    Parameters
    ----------
    port : int
        port assigned to the socket.
    host : str, optional
        host assigned to the socket. The default is ''.

    Returns
    -------
    tcpsock : socket
        socket connected at (host, port).

    """
    tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcpsock.bind((host, port))
    return tcpsock