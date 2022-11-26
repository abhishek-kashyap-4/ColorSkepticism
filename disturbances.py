# -*- coding: utf-8 -*-
"""
Created on Fri Nov 18 21:51:17 2022

@author: kashy
"""
import cv2


class disturbances:
    '''
    How do I differentiate the ones that can only return a gray vs the ones that 
    can return RGB?
    why do you need the rgb again?
    RGB is calculated for different similarity. 
    make a note of this, it will be random. 
    
    EVERY disturbance has to be differnt.
    Please don't use differnt methonds for the same kind of disturbance. 
    
    '''
    def __init__(self):
        '''use eval(methods_avail[i][0])(args) 
        to nicely call the function with your args!
        you may have to use getaatr(self,self.methods_avail[i][0])(args)
        or globals()['bar']
        
         list of tuples: 
            (arg1rangemin , arg1rangemax) , 
            (arg2rangemin, arg2rangemax)...
        note, the functions that change to gray has to come AFTER others. 
        note, functions taking 2 imgs are seperate and need to be called individually
        always return image lists'''
        self.methods_avail = [
           [ 'rotation',(0,360)],
           ['blur',(0,2),(1,10),(1,10)]
            ]
        
    def rotation(self,img, degrees):
      # divide by 360, take remainder. 
      if (degrees > 360):
        degrees = degrees % 360
      height, width = img.shape
      center = (width/2,height/2)
      R_M = cv2.getRotationMatrix2D(center,degrees,1)
      r_im = cv2.warpAffine(img,R_M,(width,height))
      
      return r_im
    def image_rotation(self,img , degrees):
        '''
        rotates image clockwise
        returns rgb.
        '''
        
    def image_mirroring(self,img , degree):
        '''
        mirros image across degree
        '''
    def blur(self,img, blurtype , blurquant, guassianoptional):
        '''
        blurtype = 0 : blur, 1: Guassianblur, 2: medianblur
        use blurquant,blurquant for kernel, guassianoptional for 1. 
        you can use blurquant, guassianoptional as kernel for others. 
        '''
        blurtype = round(blurtype)
        blurquant = round(blurquant)
        guassianoptional = round(guassianoptional)
        if(blurquant%2==0):
            blurquant+=1
        if(blurtype == 0):
            return cv2.blur(img , (blurquant , guassianoptional))
        elif(blurtype==1):
            return cv2.GaussianBlur(img , (blurquant,blurquant) , guassianoptional)
        elif(blurtype==2):
            return cv2.medianBlur(img , blurquant)
            
            
            
    def image_stitch(self,img,weight):
        
        '''
        weight decides how much soft stitching needs to be done
        '''
    def single_main(self,img,certainity_array):
        '''
        certainity array is 2d. 
        Each row has a tuple corresponding to:
            inputs for the respective function.
            There are 4 cases: (IG 1 and 4 are same.)
            [
                [True , (1,2,3)],
                [False ]
                [True]
                [True , (1)]
                ]
        
        '''
        img   = cv2.cvtColor(img , cv2.COLOR_RGB2GRAY)
        for i in range(len(certainity_array)):
            val = certainity_array[i]
            if(not val[0]):
                continue
            else:
                method_row = self.methods_avail[i]
                if(len(val)==1):
                    img = getattr(self,method_row[0])(img)
                else:
                    #every parameter for the function needs to be inside the pre-set range. 
                    
                    assert 0==sum(1  for i in range(len(val[1])) if(val[1][i]<method_row[i+1][0] or val[1][i]>method_row[i+1][1] ))
                    img = getattr(self,method_row[0])(img,*val[1])
                #output_imgs.append(output)
        return img
    def multiple_main(self, img_list):
        '''
        pick a multiple function at random
        call, 
        return image. 
        '''
        
    
        
                    
            
            
            
            
        