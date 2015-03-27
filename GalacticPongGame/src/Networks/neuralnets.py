'''
Created on Mar 25, 2015

@author: Ankur
'''

import pickle,time
from numpy import loadtxt
from pybrain.tools.shortcuts        import buildNetwork
from pybrain.supervised.trainers    import BackpropTrainer
from pybrain.datasets.supervised    import SupervisedDataSet

class CNeuralNet:
    def __init__(self,learningrate = 0.1,inputneurons = 2,hiddenneurons = 50,outputneurons = 2,testondata= True, \
                 momentum = 0.9):
        """
        Neural networks class
        assign a learning rate of your choice , default is 0.01
        inputneurons = number of neurons on input layer: can be set to the input dimension of the data
        hiddenneurons= keep it more than inputneurons in general
        outputneurons = output dimension of your data
        testondata = If you want to print out the performance of your neural net, defaults to true
        """
        assert (hiddenneurons > inputneurons), "Number of hiddenneurons can't be lesser than inputneurons"
        
        self.learningrate = learningrate
        self.inputneurons = inputneurons
        self.hiddenneurons = hiddenneurons
        self.outputneurons = outputneurons

        #momentum is the parameter to realize how efficiently the learning will get out of a local minima, 
        #not sure what to put as an appropriate value
        self.momentum = momentum

        #Construct network here
        self.mlpnetwork  = buildNetwork(self.inputneurons, self.hiddenneurons, self.outputneurons, bias=True)
        self.mlpnetwork.sortModules()
        self.trainer = None
        self.validation = testondata
        self.data = None
        
        self.learnedNetwork = None
    
    
    def train(self,filename,trainepochs = 1000):
        """
        train: call this function to train the network
        inputdata = set of input params
        trainepochs = number of times to iterate through this dataset
        """
        
        self.trainer = BackpropTrainer(self.mlpnetwork, learningrate=self.learningrate, momentum=self.momentum)
        self.trainer.trainUntilConvergence(verbose=True, dataset=self.data, maxEpochs=trainepochs)
        
        fl = filename.split('.log')[0] +str(time.strftime('%H_%M_%S'))+ "_learned.pickle"
        with open(fl, "wb") as f:
            pickle.dump(self.mlpnetwork, f)
        
    def loadTrainedModel(self, pickleFile=None):
        """
        call this function to load the trained model  
        Please call loadTrainedModel once, before calling predict, so as to load the trained model and then predict things :)       
        """

        if pickleFile == None:
            # If there are many pre-computed neural-nets, load the first one
            from glob import glob
            pickleFile = glob("../Game/outdata/*.pickle")[0]

        assert '.pickle' in pickleFile, "Invalid Neural-Net loaded..."
        with open(pickleFile, "rb") as f:
            self.mlpnetwork = pickle.load(f)
        
        return self.mlpnetwork
            
            
    def predict(self, testData):
        """
        testData = input data which is to be predicted on a given trained model
        if you trained the model earlier and want to reuse it
        """

#        assert (self.trainer != None) , "Train the model before you predict with it..."                    
        return self.mlpnetwork.activate(testData)
    
    
    def createTrainingData(self,filename,inputdim, outputdim):
        """
        create training data by reading our log file
        inputdim = inputdimension of data
        outputdim = output dim expected
        """
        
        self.data = SupervisedDataSet(inputdim,outputdim)
        textFile = loadtxt(filename, delimiter=",")
        
        for line in textFile:
            self.data.addSample(line[:inputdim], line[-outputdim:])
        
