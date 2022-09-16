# -*- coding: utf-8 -*-
"""
Created on Tue Jun 21 19:57:16 2022

@author: CRISTIAN
"""

import cv2
import os
import math
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from PIL import Image
from imutils import paths
import numpy as np
import argparse
import os

input_images_path = "D:/OPENCV/dataset/data"
files_names = os.listdir(input_images_path)


labels = []
huMoments= []

for file_name in files_names:
    #print(file_name)
    image_path = input_images_path + "/" + file_name
    print(image_path)
    image = cv2.imread(image_path)
    gris = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    # Threshold image
    _,gris = cv2.threshold(gris, 128, 255, cv2.THRESH_BINARY_INV)

    # Calculate Moments
    moments = cv2.moments(gris)
    
    # Calculate Hu Moments
    huMoments.append(cv2.HuMoments(moments))
    
#tratamientos de los momentos de Hu
hu2=np.array(huMoments)
momentshu= np.array(hu2[:,:,0])

#Log scale hu moments
for i in range(momentshu.shape[0]):
    for j in range (0,7):
        momentshu[i][j]= -1* math.copysign(1.0,momentshu[i][j]) * math.log10(abs(momentshu[i][j]))
    
#normalizo los momentos de Hu
min_max_scaler = MinMaxScaler() 
moments_hu = min_max_scaler.fit_transform(momentshu)

#particion de los momentos de hu para posteriormente entrenar y testear

#(trainX, testX, trainY, testY) = train_test_split(momentshu,test_size=0.25)
# cv2.imshow("Image", image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()