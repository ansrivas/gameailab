'''
Created on Mar 18, 2015

@author: ankur
'''
import logging 
import time
class Output:
    def __init__(self):
        ''' 
        level could be passed 
        '''
        self.logger = logging.getLogger(__name__)
        
        self.logger.setLevel(logging.INFO)

        # create a file handler
        self.filename = time.strftime('%H_%M_%S')
        self.filename = "output_"+str(self.filename) + ".log"
         
        handler = logging.FileHandler(self.filename)
        handler.setLevel(logging.INFO)

        self.logger.addHandler(handler)
    
    
    def writeLog(self, msg):

        self.logger.info(msg)
        
