# -*- coding: utf-8 -*-
"""
Created on Sat Nov 19 18:37:28 2022

@author: kashy
"""
from richzhang.colorizers import eccv16 , siggraph17
from richzhang.colorizers.util import load_img , resize_img , preprocess_img , postprocess_tens
import numpy as np
import torch
import cv2
import matplotlib.pyplot as plt

class model_of_models:
    def __init__(self):
        self.models = ['richzhang_eccv16' , 'richzhang_siggraph17']
          
    def richzhang(self,gray_img):
        colorizer_eccv16 = eccv16(pretrained=True).eval()
        colorizer_siggraph17 = siggraph17(pretrained=True).eval()
        temp_img = np.tile(gray_img[:,:,None],3) 
        (tens_l_orig, tens_l_rs) = preprocess_img(temp_img, HW=(256,256))
        img_bw = postprocess_tens(tens_l_orig, torch.cat((0*tens_l_orig,0*tens_l_orig),dim=1))
        out_img_eccv16 = postprocess_tens(tens_l_orig, colorizer_eccv16(tens_l_rs).cpu())
        out_img_siggraph17 = postprocess_tens(tens_l_orig, colorizer_siggraph17(tens_l_rs).cpu())
        return out_img_eccv16 , out_img_siggraph17
    def main(self , gray_img):
        #gray_img = cv2.cvtColor(gray_img , cv2.COLOR_GRAY2RGB)
        a,b = self.richzhang(gray_img)
        retval = {'richzhang_eccv16':a , 'richzhang_siggraph17':b}
        return retval



        