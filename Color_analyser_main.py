# -*- coding: utf-8 -*-
"""
Created on Sun Nov 20 08:41:32 2022

@author: kashy
"""

from model_of_models import model_of_models
import matplotlib.pyplot as plt
import cv2
import numpy as np
import pandas as pd
from disturbances import disturbances
import os
import sys
import random
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
def get_certainity_string(methods_avail):
    
    #Currently, the probability of each method is uniformly random. 
    #This can be changed to normal random, or any other thing in the future.
    probability_array= [random.random() for x in range(len(methods_avail))]
    certainity_string = []
    for i in range(len(probability_array)):
        val = probability_array[i]
        parameter_ranges = methods_avail[i][1:] #1st one is the method name. Here, its inconsequencial.
        if(val>= random.random()):
            if(len(parameter_ranges)==0):
                certainity_string.append([True])
            else:
                parameters = [random.uniform(t[0] ,t[1])  for t in parameter_ranges]
                certainity_string.append([True,parameters])
                
        else:
            certainity_string.append([False])
            
        
    
    return certainity_string

def reset_disturbance_id(input_image_id):
    with open('autogen_vars.txt','w') as f:
        f.write('id1:'+str(input_image_id)+'\nid2:1000\nalways end with this line.')

def update_disturbances_csv():
    '''
    Low priority. 
    any nan values in the output columns need to be updated with values.
    you get the values by reading the image in id column, 
    recoloring it with model, 
    saving it in images_recolored,
    finding similarity and adding it .
    '''
def read_disturbances_csv(disturbances_obj , model_of_models_obj):
    '''
    read csv , 
    from disturbances_obj.methods_avail, get column names
    if there's only one parameteer, column name = function name. 
    if there are more, column name = function name _ parametercounter.
    
    if any new disturbances added, add column with zeros
    if new model_of_models_obj added, add column with Nones
    return csv
     REMEMBER: you still haven't handled multiple image takers here. 
                 these won't be in the dataframe just yet.
        
    '''
    disturbances = pd.read_csv('disturbances.csv')
    column_names = []
    for methodrow in disturbances_obj.methods_avail:
        columnname = methodrow[0]
        params = methodrow[1:]
        if(len(params)<2):
            column_names.append(columnname)
        else:
            for i in range(len(params)):
                column_names.append(columnname+'_'+str(i))
    for column in column_names:
        if(column not in disturbances.columns):
            disturbances[column] = 0
    
    for model in model_of_models_obj.models:
        if('output_'+model not in disturbances.columns):
            disturbances['output_'+model] = 'Null'
    return disturbances

    

with open('autogen_vars.txt','r') as f:
    autogen_vars = f.readlines()

input_image_id = int(autogen_vars[0].split(':')[1][:-1])
disturbance_id = int(autogen_vars[1].split(':')[1][:-1])

disturbances_obj = disturbances() 
model_of_models_obj  = model_of_models()
if(input('Did you close the csv, and autogen vars? Enter 0 to exit') == '0'):
    sys.exit(0)
disturbances_csv = read_disturbances_csv(disturbances_obj,model_of_models_obj)
figureval = 0
stop_after_iternations = 20
reusability = 3 #Make these many disturbance to 1 image. this will create 10 disturbed images for each input image.
for filename in os.listdir('images_input'):
    
    
    if(not (filename.endswith('jpg') or  filename.endswith('jpeg') or  filename.endswith('png'))):
        print('Are there files that are not images in images_input?')
        sys.exit(0)
    if(stop_after_iternations<=0):
        print('stopping after limit iterations')
        break
    stop_after_iternations -=1
    reset_disturbance_id(input_image_id)
    disturbance_id = 1000
    img = cv2.imread(os.path.join('images_input',filename))
    img = cv2.cvtColor(img , cv2.COLOR_BGR2RGB)

    input_image_id +=1 
    plt.imsave('images_input_processed/%s.jpg'%input_image_id , img)
    #########os.remove('images_input/'+filename)
    for iii in range(reusability):    
        certainity_array = get_certainity_string( disturbances_obj.methods_avail )
        try:
            disturbed_image = disturbances_obj.single_main(img , certainity_array)
        except AssertionError:
            print('Assertion Error')
            break
        
        disturbance_id += 1
        image_id = '{}_{}'.format(input_image_id ,disturbance_id )
        plt.imsave('images_disturbed/{}.jpg'.format(image_id) , disturbed_image,cmap='gray')
        d={'image_id':image_id}
        
        for j in range(len(certainity_array)):
            flag = certainity_array[j][0]
            funct = disturbances_obj.methods_avail[j][0]
            params = certainity_array[j][1:]
            params2 = disturbances_obj.methods_avail[j][1:]
            #I HANDLED CERTAINITY ARRAY AND METHODS VAL SLIGHTLY DIFFERENTLY
            if(len(params2)<2):
                d[funct] = int(flag)
            else:
                for i in range(len(params2)):
                    if(not flag):
                        d[funct+'_'+str(i)] = 0
                    else:
                        d[funct+'_'+str(i)] = params[0][i]
        #ORIGINAL GREY IMAGE
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        img_dict = model_of_models_obj.main(disturbed_image)
        for model in img_dict:
            plt.imsave('images_recolored/{}_{}.jpg'.format(image_id,model) , img_dict[model])
            
        disturbances_csv = disturbances_csv.append(d,ignore_index = True)
            
disturbances_csv.to_csv('disturbances.csv')      
with open('autogen_vars.txt','w') as f:
    f.write('id1:'+str(input_image_id)+'\nid2:'+str(disturbance_id)+'\nalways end with this line.')
     

1/0






disturbances_obj = disturbances()


obj = model_of_models()

im = cv2.imread('examples/kettle_toast_palette.jpg')
plt.figure(1)
plt.imshow(cv2.cvtColor(im , cv2.COLOR_BGR2RGB))
gray = cv2.cvtColor(im , cv2.COLOR_BGR2GRAY)


plt.figure(2)
plt.imshow(a)
plt.figure(3)
plt.imshow(b)
        