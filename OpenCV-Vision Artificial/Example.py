# -*- coding: utf-8 -*-
"""
Created on Wed Jun 22 17:26:52 2022

@author: CRISTIAN
"""
import cv2

image = cv2.imread("10.png")
gris = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
# Threshold image
_,gris = cv2.threshold(gris, 128, 255, cv2.THRESH_BINARY_INV)

(alto,ancho,canales) = image.shape
# #redimensionamiento proporcional
r = 300/ancho
dim = (300, int(alto*r))
redimp = cv2.resize(gris,dim)

# Calculate Moments
moments = cv2.moments(redimp)
# Calculate Hu Moments
hu=cv2.HuMoments(moments)
while True:
    cv2.imshow('Imagen',redimp)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()