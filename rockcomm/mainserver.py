#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .datasave import DataSaver
from .connexionthread import DatarcvThread, CommandThread, UserThread, InfoThread
from .manager import CommandManager, InfoManager

from time import sleep

from os import getcwd

class MainServer(): #MUST GET DATA SAVING IN THIS
    """
    Main server class - can handle communication with machine, user and data saving.
    """
    def __init__(self, host, commandPort, dataPort, userPort, infoPort):
        """


        Parameters
        ----------
        host : str
            host of the server
        commandPort : int
            port sending commands to the machine.
        dataPort : int
            port receiving data from the machine.
        userPort : int
            port listening to the user.
        infoPort : int
            port sending automatic informations to user.

        Returns
        -------
        None.

        """
        self.host = host
        self.portC = commandPort
        self.portD = dataPort
        self.portU = userPort
        self.portI = infoPort
        self.threads = []
    
    def start(self):
        """
        Starts the server.

        Returns
        -------
        None.

        """
        self.DSaver = DataSaver(maindir=getcwd()) #MUST BE CREATED CORRECTLY
        self.DThread = DatarcvThread((self.host, self.portD), self.DSaver, listenMax=1)
        self.threads.append(self.DThread)
        self.DThread.start()
        
        self.CManager = CommandManager()

        self.UThread = UserThread((self.host, self.portU), self.CManager)
        self.threads.append(self.UThread)
        self.UThread.start()
        
        self.CThread = CommandThread((self.host, self.portC), self.CManager)
        self.threads.append(self.CThread)
        self.CThread.start()
        
        self.IManager = InfoManager()
        
        self.IThread = InfoThread((self.host, self.portI), self.IManager)
        self.threads.append(self.IThread)
        self.IThread.start()
        
        sleep(.1)
        print('Server started')
        print(self)
        return
    
    def __str__(self):
        return 'Server ports: \n - data receiving: {}\n - command sending :{}\n - user receiving: {}\n - information sending: {}'.format(self.portD, self.portC, self.portU, self.portI)
        
    def stop(self):
        """
        Shutdowns the connexions.

        Returns
        -------
        None.

        """ 
        for thread in self.threads:
            thread.stopconnexion()
            thread.join()
        print("Server shut down.")
        return