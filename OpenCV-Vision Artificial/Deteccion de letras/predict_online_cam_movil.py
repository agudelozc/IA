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
import time
# import the opencv library
from joblib import dump, load
from sklearn.preprocessing import MinMaxScaler
from keras.models import load_model
import tensorflow as tf

clf = load('maquinas.joblib') 

#model = load_model('modelo_exportado.h5')
# model.compile(
#     optimizer='adam',
#     loss=tf.keras.losses.SparseCategoricalCrossentropy(),
#     metrics=['accuracy']
# )
#model = load_model('myModel2806222.h5')
# Replace the below URL with your own. Make sure to add "/shot.jpg" at last.
url = "http://192.168.1.1:8080/shot.jpg"

seguidor = 0
acumuladorclase0 = 0
acumuladorclase1 = 0
acumuladorclase2 = 0

# While loop to continuously fetching data from the Url
while True:
    time.sleep(2)
    img_resp = requests.get(url)
    img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
    img = cv2.imdecode(img_arr, -1)
    img = imutils.resize(img, width=1000, height=1800)
    gris = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    # Threshold image
    _,gris = cv2.threshold(gris, 100, 255, cv2.THRESH_BINARY_INV)

    hu=np.array([])

    contours, hierarchy = cv2.findContours(gris, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    cv2.putText(img,'Objetos clase 0 :',(600,100),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0))
    cv2.putText(img,'Objetos clase 1 :',(600,150),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0))
    cv2.putText(img,'Objetos clase 2 :',(600,200),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255))
    
    conteocuadro  = 0
    for i in contours:
         area = cv2.contourArea(i)
         #if area >20000 and area <100000: 
         if area >5000 and area <25000:
             conteocuadro+=1
             x,y,w,h = cv2.boundingRect(i)
             roi = gris[y:y+h,x:x+w]
             #Calculate Moments
             moments = cv2.moments(roi)
              #Calculate Moments
              #Calculate Hu Moments
             huMoments = cv2.HuMoments(moments)
               #Log scale hu moments
             for j in range(0,7):
                  huMoments[j] = (-1* math.copysign(1.0, huMoments[j]) * math.log10(abs(huMoments[j])))
                  hu = huMoments.T
                  min_max_scaler = MinMaxScaler() 
                  moments_hu = min_max_scaler.fit_transform(hu.T)
             print(f'moments hu : {hu}')
             #predict_x=model.predict(moments_hu.T)
             #resultado=np.argmax(predict_x,axis=1)
             resultado=clf.predict(moments_hu.T)
             print(f'Prediccion = {resultado}')
             
             cont0=False
             cont1=False
             cont2=False
             
             if resultado==[0]:
               x,y,w,h = cv2.boundingRect(i)
               cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 3)
               cont0=True
             if resultado ==[1]:
               x,y,w,h = cv2.boundingRect(i)
               cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 3)
               cont1=True
             if resultado ==[2]:
               x,y,w,h = cv2.boundingRect(i)
               cv2.rectangle(img, (x,y), (x+w,y+h), (0,0,255), 3)
               cont2=True
               
    if conteocuadro>seguidor and cont0==True:
        acumuladorclase0=acumuladorclase0+(conteocuadro-seguidor)
        
    elif conteocuadro>seguidor and cont1==True:
        acumuladorclase1=acumuladorclase1+(conteocuadro-seguidor)
        
    elif conteocuadro>seguidor and cont2==True:
        acumuladorclase2=acumuladorclase2+(conteocuadro-seguidor)
        
    seguidor = conteocuadro

    
    cv2.putText(img,f'{acumuladorclase0}',(900,100),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0))  
    cv2.putText(img,f'{acumuladorclase1}',(900,150),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0)) 
    cv2.putText(img,f'{acumuladorclase2}',(900,200),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255)) 

    cv2.imshow("Android_cam",img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
       break
  
cv2.destroyAllWindows()