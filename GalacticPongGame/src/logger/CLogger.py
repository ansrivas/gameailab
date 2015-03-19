'''
Created on Mar 18, 2015

@author: ankur
'''
import logging 

class Output:
    def __init__(self):
        ''' 
        level could be passed 
        '''
        self.logger = logging.getLogger(__name__)
        
        self.logger.setLevel(logging.INFO)

        # create a file handler
        
        handler = logging.FileHandler('outputdata.log')
        handler.setLevel(logging.INFO)
        
        # create a logger format
        
        #formatter = log.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        #handler.setFormatter(formatter)
        
        # add the handlers to the logger
        self.logger.addHandler(handler)
    
    
    def writeLog(self,msg):
        self.logger.info(msg)
        
#logger.info('Hello baby')