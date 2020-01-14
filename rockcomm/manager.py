#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from numpy.random import rand
from threading import Thread
from time import sleep

class CommandManager():
    """
    manages the commands sent by the user.
    """
    def __init__(self):
        self.commands_to_proc = {}
        self.answers = {}
        
    def add_command(self, command):
        """
        add a command to process.

        Parameters
        ----------
        command : bytes (binary str)
            command to add.

        Returns
        -------
        key : float
            random number in [0;1]. Key to access the answer to the command.

        """
        key = rand()
        self.commands_to_proc[key] = command
        self.answers[key] = None
        return key
    
    def get_command(self, destination):
        """
        get the oldest command for the destination to process and its key.
        
        Parameters
        ----------
        destination : str
            who the command is for; should be 'SERV' or 'MACH'.
        
        Returns
        -------
        key : float
            the command's key.
        bytes (binary str)
            the command.

        """
        for key in self.commands_to_proc:
            command = self.commands_to_proc[key]
            if command[-4:] == destination.encode():
                return (key, command)
        return (None, None)

    def add_answer(self, key, answer):
        """
        add an answer.

        Parameters
        ----------
        key : float
            the answered command's key.
        answer : bytes (binary str)
            the answer to add.

        Returns
        -------
        None.

        """
        del(self.commands_to_proc[key])
        self.answers[key] = answer
        return



class PeriodicInfo(Thread):
    """
    Info sent periodically to the user
    """
    def __init__(self, info, period, IManager, continuous = True):
        """

        Parameters
        ----------
        info : bytes (binary str)
            the information.
        period : float
            period of sending (in seconds).
        IManager : InfoManager
            the InfoManager that will manage the information.
        continuous : bool, optional
            whether to continue sending. The default is True.

        Returns
        -------
        None.

        """
        self.info = info
        self.period = period
        self.continuous = True
        return
    
    def run(self):
        while(self.continuous):
            self.IManager.add_info(self.info)
            sleep(self.period)
        return
    
    def stopsend(self):
        """
        stops sending at the end of the current period.

        Returns
        -------
        None.

        """
        self.continuous = False
        return


    
class InfoManager():
    """
    Manages the informations to automatically send to the user.
    """
    def __init__(self):
        self.info_to_send = []
        self.periodic_infos = {}
        return
    
    def add_info(self, info):
        """
        add a new information to send.

        Parameters
        ----------
        info : bytes (binary str)
            the new information.

        Returns
        -------
        None.

        """
        self.info_to_send.append(info)
        return
    
    def add_periodic_info(self, info, period):
        """
        add an information to send periodically.

        Parameters
        ----------
        info : bytes (binary str)
            the information.
        period : float
            period of sending (in seconds).

        Returns
        -------
        key : float
            key to access the periodic information later.

        """
        NewPeriodInfo = PeriodicInfo(info, period, self)
        key = rand()
        self.periodic_infos[key] = NewPeriodInfo
        NewPeriodInfo.start()
        return key
    
    def remove_periodic_info(self, key):
        """
        stops the sending of a periodic information.

        Parameters
        ----------
        key : float
            the information's key.

        Returns
        -------
        None.

        """
        Info_to_stop = self.periodic_infos[key]
        Info_to_stop.stopsend()
        del(self.periodic_infos[key])
    
    def get_info(self):
        """
        get the oldest information to send

        Returns
        -------
        info : bytes (binary str) or None
            the information to send - or None if there is nothing to send.

        """
        if self.info_to_send == []:
            return None
        info = self.info_to_send[0]
        del(self.info_to_send[0])
        return info