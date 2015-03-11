'''
Created on Mar 7, 2015

@author: Sridev
'''
def fadeOUT(image,ColorTone):
    
    FadeINspeed = 5        
    image.set_alpha(ColorTone)            
    ColorTone -= FadeINspeed
            
    return image,ColorTone