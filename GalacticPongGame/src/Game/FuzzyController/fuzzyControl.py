import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt

class Fuzzy():
    
    def __init__(self):
        # Generate universe functions
        self.distance = np.arange(0.,181.,1.)
        self.acceleration = np.arange(0.,0.1,0.01)
        
        # Generate Distance membership functions
        self.near = fuzz.trapmf(self.distance, (-1.,-1.,20.,65.))
        self.medium = fuzz.trapmf(self.distance,(35.,80.,120.,135.))
        self.far = fuzz.trapmf(self.distance,(105.,170.,180.,200.))
        
        # Generate Acceleration membership functions
        self.slow = fuzz.trimf(self.acceleration, (-1.,0.,0.05))
        self.normal = fuzz.trapmf(self.acceleration,(0.02,0.035,0.04,0.07))
        self.fast = fuzz.trapmf(self.acceleration,(0.06,0.085,0.1,0.2))
    
        # Fuzzy relation
        self.R1 = fuzz.relation_product(self.near,self.slow)
        self.R2 = fuzz.relation_product(self.medium,self.normal)
        self.R3 = fuzz.relation_product(self.far,self.fast)
        
        
        # Combine the fuzzy relation
        self.R_combined = np.fmax(self.R1, np.fmax(self.R2, self.R3))
        
        self.thetaOne = 0.0
        self.thetaTwo = 0.0
        
        self.InputDistanceAngle = 0.0
        self.OutputAcceleration = 0.0
        
        
        self.visualize = True
    
    def getFuzzyAcceleration(self,currentBatAngle,predictedBatAngle):
        
        self.thetaOne = abs(currentBatAngle-predictedBatAngle)
        self.thetaTwo = currentBatAngle + (360-predictedBatAngle)
        
        if(self.thetaOne < self.thetaTwo):
            self.InputDistanceAngle = self.thetaOne
        else:
            self.InputDistanceAngle = self.thetaTwo
            
        self.InputDistanceAngle = int(self.InputDistanceAngle)
            
        print self.InputDistanceAngle
            
        self.OutputAcceleration = fuzz.defuzz(self.acceleration,self.R_combined[self.distance == self.InputDistanceAngle], 'centroid')
        
        print self.InputDistanceAngle,self.OutputAcceleration
        
        return self.OutputAcceleration
    
        self.predicted_acceleration = np.zeros_like(self.distance)

        for i in range(len(self.predicted_acceleration)):
            self.predicted_acceleration[i] = fuzz.defuzz(self.acceleration, self.R_combined[i, :], 'centroid')
            
        if(self.visualize):
            
            # Visualize Input - Distance
            self.fig,self.ax = plt.subplots()
            
            self.ax.plot(self.distance,self.near,'b',self.distance,self.medium,'g',self.distance,self.far,'r')
            self.ax.set_ylabel('Fuzzy Membership')
            self.ax.set_xlabel('Distance')
            self.ax.set_ylim(-0.05,1.05)
            plt.show()
            plt.savefig('Distance.png')
            
            # Visualize Output - Acceleration
            self.fig1,self.ax1 = plt.subplots()
            
            self.ax1.plot(self.acceleration,self.slow,'b',self.acceleration,self.normal,'g',self.acceleration,self.fast,'r')
            self.ax1.set_ylabel('Fuzzy Membership')
            self.ax1.set_xlabel('Acceleration')
            self.ax1.set_ylim(-0.05,1.05)
            plt.show()
            plt.savefig('Acceleration.png')
            
            self.plt.plot(self.distance, self.predicted_acceleration, 'k')
            self.plt.xlabel('Distance')
            self.plt.ylabel('Acceleration')
            self.plt.show()
            plt.savefig('Prediction.png')