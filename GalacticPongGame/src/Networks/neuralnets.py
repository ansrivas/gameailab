'''
Created on Mar 25, 2015

@author: Ankur
'''


from pybrain.tools.shortcuts import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
import pickle ,numpy as np
 
from pybrain.datasets.supervised import SupervisedDataSet

class CNeuralNet:
    def __init__(self,learningrate = 0.01,inputneurons = 2,hiddenneurons = 50,outputneurons = 2,testondata= True):
        """
        Neural networks class
        assign a learning rate of your choice , default is 0.01
        inputneurons = number of neurons on input layer: can be set to the input dimension of the data
        hiddenneurons= keep it more than inputneurons in general
        outputneurons = output dimension of your data
        testondata = If you want to print out the performance of your neural net, defaults to true
        """
        if(hiddenneurons < inputneurons):
            raise Exception("Number of hiddenneurons can't be lesser than inputneurons")
        
        
        
        
        self.learningrate = learningrate
        self.inputneurons = inputneurons
        self.hiddenneurons = hiddenneurons
        self.outputneurons = outputneurons

        #Construct network here
        self.mlpnetwork  = buildNetwork(self.inputneurons, self.hiddenneurons, self.outputneurons, bias=True)
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
        #momentum is the parameter to realize how efficiently the learning will get out of a local minima, 
        #not sure what to put as an appropriate value
        
        self.trainer = BackpropTrainer(self.mlpnetwork, learningrate =self.learningrate, momentum = 0.99)
     
        self.trainer.trainUntilConvergence(verbose=True, dataset=self.data, maxEpochs=trainepochs)
        #self.trainer.trainOnDataset(self.data, trainepochs)
        #if(self.validation):
        #    self.trainer.testOnData()
        filename = filename + "_learned"
        f = open(filename, 'wb')
        pickle.dump(self.mlpnetwork, f)
        f.close()   

        
     
    def loadTrainedModel(self):
        """
        call this function to load the trained model
        """
                
        try:
            f = open('rb')
            self.mlpnetwork = pickle.load(f)
            f.close()
        except:
            raise Exception("File not found, or something happened, i dont know")
            
            
    def predict(self,learnedfile,d):
        """
        Please call loadTrainedModel once, before calling predict, so as to load the trained model and then predict things :)
        
        d = input data which is to be predicted on a given trained model
        if you trained the model earlier and want to reuse it
        """
                    
        return self.mlpnetwork.activate(d)
    
    
    def createTrainingData(self,name,inputdim, outputdim):
        """
        create training data by reading our log file
        inputdim = inputdimension of data
        outputdim = output dim expected
        """
        
        self.data = SupervisedDataSet(inputdim,outputdim)
        temp = np.loadtxt(name, delimiter=",")
        
        for i in temp:
            self.data.addSample(i[:5], i[7:])

        
        

        
        
        
        