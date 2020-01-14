#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#from os import getcwd

class Data():
    """
    Data object.
    """
    def __init__(self, dtype, dvalue, timeofsave=None):
        """
        

        Parameters
        ----------
        dtype : str
            type of the data.
        dvalue : any type
            value of the data - type depends on the dtype.
        timeofsave : TYPE, optional
            DESCRIPTION. The default is None.

        Returns
        -------
        None.

        """
        
        self.dtype = dtype
        self.dvalue = dvalue
        self.timeofsave = timeofsave
    
    def save(self, datasaver):
        datasaver.save(self)
        return
