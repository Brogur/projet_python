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


"""
class DataSaver():
    """
    Object allowing to save every data.
    """
    def __init__(self, datatypes=[], maindir=getcwd()+'/data'):
        """
        

        Parameters
        ----------
        datatypes : list, optional
            List of currently received data types. The default is [].
        maindir : str, optional
            main directory where to save the data files. The default is getcwd()+'/data'.

        Returns
        -------
        None.

        """
        self.maindir = maindir
        self.paths = [[maindir+'/{}.txt'.format(dtype), dtype] for dtype in datatypes]
        self.writers = {path[1] : open(path[0], 'a') for path in self.paths}
        return
    
    def addDtype(self, dtype):
        """
        adds a new data type

        Parameters
        ----------
        dtype : str
            data type to add.

        Returns
        -------
        None.

        """
        newpath = [self.maindir+'/{}.txt'.format(dtype), dtype]
        if newpath not in self.paths:
            self.paths.append(newpath)
            self.writers[dtype] = open(newpath[0], 'a')
        return
    
    def save(self, dataObj):
        """
        saves a new data.

        Parameters
        ----------
        dataObj : Data
            data to save.

        Returns
        -------
        None.

        """
        while True:
            try:
                with self.writers[dataObj.dtype] as fichier:
                    fichier.write('{}   {}\n'.format(dataObj.timeofsave, dataObj.dvalue))
            except KeyError:
                self.addDtype(dataObj.dtype)
            except ValueError:
                for path in self.paths:
                    if path[1] == dataObj.dtype:
                        path_to_open = path[0]
                        break
                self.writers[dataObj.dtype] = open(path_to_open, 'a')
            else:
                break
        return
        """
