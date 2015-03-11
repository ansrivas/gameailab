'''
Created on Mar 6, 2015

@author: Sridev
'''
def fadeIN(image,ColorTone):
    
    FadeINspeed = 5        
    image.set_alpha(ColorTone)            
    ColorTone += FadeINspeed
            
    return image,ColorTone
    