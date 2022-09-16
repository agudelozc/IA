# -*- coding: utf-8 -*-
"""
Created on Tue Jun 28 18:01:11 2022

@author: CRISTIAN
"""
import numpy as np

import os
import cv2
import math
from sklearn.preprocessing import MinMaxScaler
import re
#import matplotlib.pyplot as plt
from sklearn import svm, metrics
from sklearn.neural_network import MLPClassifier
import tensorflow as tf
import imutils

while True:
    huMoments = []
    image = cv2.imread('10.jpg')
    image = imutils.resize(image, width=1000, height=1800)
    gris = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    # Threshold image
    _,gris = cv2.threshold(gris, 100, 255, cv2.THRESH_BINARY_INV)
    
    hu=np.array([])
    
    contours, hierarchy = cv2.findContours(gris, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for i in contours:
        area = cv2.contourArea(i)
        if area >20000 and area <100000:
            x,y,w,h = cv2.boundingRect(i)
            roi = gris[y:y+h,x:x+w]
            #Calculate Moments
            # Calculate Moments
            moments = cv2.moments(roi)      
            # Calculate Hu Moments
            huMoments.append(cv2.HuMoments(moments))  
            #tratamientos de los momentos de Hu
            hu2=np.array(huMoments)
            momentshu= np.array(hu2[:,:,0])
            
            # #Log scale hu moments
            for i in range(momentshu.shape[0]):
                for j in range (0,7):
                    momentshu[i][j]= -1* math.copysign(1.0,momentshu[i][j]) * math.log10(abs(momentshu[i][j]))
                    
    cv2.imshow("Android_cam",roi)
    if cv2.waitKey(1) & 0xFF == ord('q'):
               break
cv2.destroyAllWindows()