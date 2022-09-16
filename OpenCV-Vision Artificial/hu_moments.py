# -*- coding: utf-8 -*-
"""
Created on Tue Jun 21 17:43:21 2022

@author: CRISTIAN
"""
import cv2
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import math
import os


#------CARGA DE IMAGENES----------
imagen = cv2.imread('logo.png')
#----CONVERTIR IMAGEN A ESCALA DE GRISES----
gris = cv2.cvtColor(imagen,cv2.COLOR_BGR2GRAY)
# Threshold image
_,gris = cv2.threshold(gris, 128, 255, cv2.THRESH_BINARY_INV)

# Calculate Moments
moments = cv2.moments(gris)
# Calculate Hu Moments
huMoments = cv2.HuMoments(moments)

# Log scale hu moments
for i in range(0,7):
    huMoments[i] = (-1* math.copysign(1.0, huMoments[i]) * math.log10(abs(huMoments[i])))
    
#normalizo los momentos de Hu
min_max_scaler = MinMaxScaler() 
dfhumoments = min_max_scaler.fit_transform(huMoments)
#dfhumoments = pd.DataFrame(dfhumoments) # Convertimos a Dataframe
cv2.imshow('Imagen',imagen)
cv2.waitKey(0)