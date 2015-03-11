'''
Created on Mar 6, 2015

@author: Sridev
'''
def fadeIN(image,ColorTone,imageList):
    
    if(image == imageList[18] or image == imageList[19] or image == imageList[20]):
        FadeINspeed = 0.6
    
    elif(image == imageList[0] or image == imageList[1] or image == imageList[2] or image == imageList[5] or image == imageList[10] or image == imageList[11]):
        FadeINspeed = 1.1 
        
    elif(image == imageList[3] or image == imageList[12] or image == imageList[13] or image == imageList[14] or image == imageList[15] or image == imageList[16] or image == imageList[17]):
        FadeINspeed = 0.8
        
    elif(image == imageList[4]):
        FadeINspeed = 2
        
    elif(image == imageList[6] or image == imageList[7] or image == imageList[8] or image == imageList[9]):
        FadeINspeed = 1.6
                
    else:    
        FadeINspeed = 5       
         
    image.set_alpha(ColorTone)            
    ColorTone += FadeINspeed
            
    return image,ColorTone
    