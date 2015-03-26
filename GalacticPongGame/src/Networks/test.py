from pybrain.datasets import SupervisedDataSet

dataModel = [
    [(0,0), (0,)],
    [(0,1), (1,)],
    [(1,0), (1,)],
    [(1,1), (0,)],
]

ds = SupervisedDataSet(2, 1)
for input, target in dataModel:
    ds.addSample(input, target)

# create a large random data set
import random
random.seed()
trainingSet = SupervisedDataSet(2, 1);
for ri in range(0,1000):
    input,target = dataModel[random.getrandbits(2)];
    trainingSet.addSample(input, target)

from pybrain.tools.shortcuts import buildNetwork
net = buildNetwork(2, 2, 1, bias=True)

from pybrain.supervised.trainers import BackpropTrainer
trainer = BackpropTrainer(net, ds, learningrate = 0.001, momentum = 0.99)
trainer.trainUntilConvergence(verbose=True, dataset=trainingSet, maxEpochs=10)
'''
print '0,0->', net.activate([0,0])
print '0,1->', net.activate([0,1])
print '1,0->', net.activate([1,0])
print '1,1->', net.activate([1,1])

'''


#learn XOR with a nerual network with saving of the learned paramaters

import pybrain
from pybrain.datasets import *
from pybrain.tools.shortcuts import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
import pickle

if __name__ == "__main__":
    ds = SupervisedDataSet(2, 1)
    ds.addSample( (0,0) , (0,))
    ds.addSample( (0,1) , (1,))
    ds.addSample( (1,0) , (1,))
    ds.addSample( (1,1) , (0,))

    net = buildNetwork(2, 4, 1, bias=True)

    try:
        f = open('_learned', 'r')
        net = pickle.load(f)
        f.close()
    except:
        #if the file is not present then do this
        trainer = BackpropTrainer(net, learningrate = 0.01, momentum = 0.99)
        trainer.trainOnDataset(ds, 1000)
        #trainer.testOnData()
        f = open('_learned', 'w')
        pickle.dump(net, f)
        f.close()
    

    #print net.activate((0,1))




