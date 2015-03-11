'''
Created on Mar 11, 2015

@author: Ankur
'''

import sqlite3 as lite
import os

class Data:
    
    def __init__(self):
        self.dbname= "players.db"
        self.dbconn = None
        self.cur = None
        if(self.fileexists()== False):
            self.opendb()
            self.createtables()
        else:
            self.opendb()
            
    '''
    this function opens the db, if not present, creates it
    '''
            
    def opendb(self):  
        self.dbconn = lite.connect('players.db')  
        self.cur = self.dbconn.cursor()
    
    def fileexists(self):
        return os.path.exists('players.db')
    
        
    '''
    this function should be called only once, if db doesn't exist
    '''
    def createtables(self):
        self.cur.execute('''CREATE TABLE score
       (ID INT PRIMARY KEY     NOT NULL,
       NAME           TEXT    NOT NULL,
       AGE            INT     NOT NULL,
       ADDRESS        CHAR(50),
       SALARY         REAL);''')

if __name__ == "__main__":
    dobj = Data()

