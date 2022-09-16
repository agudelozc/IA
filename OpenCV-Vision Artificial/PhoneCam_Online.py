# -*- coding: utf-8 -*-
"""
Created on Tue Jun 21 15:48:13 2022

@author: CRISTIAN
"""

# Import essential libraries
import requests
import cv2
import numpy as np
import imutils
import math
# import the opencv library
from joblib import dump, load
from sklearn.preprocessing import MinMaxScaler
#clf = load('filename.joblib')

# Replace the below URL with your own. Make sure to add "/shot.jpg" at last.
url = "http://192.168.1.1:8080/shot.jpg"
  
# While loop to continuously fetching data from the Url
while True:
    img_resp = requests.get(url)
    img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
    img = cv2.imdecode(img_arr, -1)
    img = imutils.resize(img, width=1000, height=1800)
    gris = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    # Threshold image
    _,gris = cv2.threshold(gris, 128, 255, cv2.THRESH_BINARY_INV)
    # #suavizar la imagen con un filtrado gaussiano
    gaussiana = cv2.GaussianBlur(gris, (3,3), 0)
    # Calculate Moments
    moments = cv2.moments(gaussiana)
    # Calculate Hu Moments
    huMoments = cv2.HuMoments(moments)
    hu=np.array([])

    # Log scale hu moments
    contours, hierarchy = cv2.findContours(gris, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.putText(img,f'Objetos clase 0:',(600,100),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0))
    cv2.putText(img,f'Objetos clase 1:',(600,150),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0))
    cv2.putText(img,f'Objetos clase 2:',(600,200),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255))
    contadorclase0=0
    contadorclase1=0
    contadorclase2=0
    for i in contours:
         area = cv2.contourArea(i)
         if area > 1000 and area < 45000:
              #Log scale hu moments
             for j in range(0,7):
                 huMoments[j] = (-1* math.copysign(1.0, huMoments[j]) * math.log10(abs(huMoments[j])))
                 hu = huMoments.T
                 min_max_scaler = MinMaxScaler() 
                 moments_hu = min_max_scaler.fit_transform(hu.T)
             
    
    cv2.imshow("Android_cam", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
       break
  
cv2.destroyAllWindows()