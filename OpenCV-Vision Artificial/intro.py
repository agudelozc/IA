# -*- coding: utf-8 -*-
"""
Created on Sat Jun 18 11:07:55 2022

@author: CRISTIAN
"""

#importacion de libreria opencv
import cv2
import numpy as np

#EJ1
#------CARGA DE IMAGENES----------
# imagen = cv2.imread('logo.png')
# cv2.imshow('Imagen',imagen)
# cv2.waitKey(0)


#EJ2
#----CONVERTIR IMAGEN A ESCALA DE GRISES----
# imagen=cv2.imread('logo.png')
# gris = cv2.cvtColor(imagen,cv2.COLOR_BGR2GRAY)
# #suavizar la imagen con un filtrado gaussiano
# gaussiana = cv2.GaussianBlur(gris, (5,5), 0)

# #Detector bordes Canny
# bordes = cv2.Canny(gaussiana,50,100)
# cv2.imshow('Imagen',bordes)
# cv2.waitKey(0)


#EJ3
#-----SEPARAR Y UNIR IMAGEN EN RGB--------
# imagen = cv2.imread('Logo.png')
# B, G, R = cv2.split(imagen)
# unidad = cv2.merge([B,G,R])
# print(imagen.shape[:2]) #los dos primeros ancho y largo
# negra = np.zeros(imagen.shape[:2],dtype='uint8')
# cv2.imshow('Imagen',cv2.merge([B,negra,negra]))
# cv2.waitKey(0)


#EJ4
#-------APLICAR UN UMBRAL A UN CANAL-----
# imagen = cv2.imread('Logo.png')
# #extrasion de canales
# B, G, R = cv2.split(imagen)
# #umbralizacion
# ret,binaria = cv2.threshold(R, 155, 255, cv2.THRESH_BINARY_INV)
# cv2.imshow('Imagen',binaria)
# cv2.waitKey(0)


#EJ5
#------APLICAR UMBRAL A IMAGEN A COLOR-----
# imagen= cv2.imread('Logo.png')
# #umbralizacion
# umbral = cv2.inRange(imagen, (84,163,0), (94,193,10))
# #umbralizacion sobre original
# extraido = cv2.bitwise_and(imagen, imagen, mask=umbral)
# cv2.imshow('Imagen',extraido)
# cv2.waitKey(0)


#EJ6
#-----ENCONTRAR,CONTAR DIBUJAR CONTORNOS-------
# imagen = cv2.imread('Logo.png')
# B,G,R = cv2.split(imagen)
# ret,binaria= cv2.threshold(R,50,255,cv2.THRESH_BINARY_INV)
# #encontrar contornos
# contornos,_=cv2.findContours(binaria,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
# print(f'La imagen original tiene la siguiente cantidad de objetos: {len(contornos)}')
# cv2.drawContours(imagen, contornos,155,(0,0,255),2)
# cv2.imshow('Imagen',imagen)
# cv2.waitKey(0)


#EJ7
#------EROSIÓN Y DILATACIO-------
# imagen = cv2.imread('Logo.png')
# B,G,R = cv2.split(imagen)
# ret,binaria= cv2.threshold(R,50,255,cv2.THRESH_BINARY_INV)
# #dilatacion y erosion
# kernel=np.ones((3,3),dtype='uint8')
# erosion=cv2.erode(binaria,kernel,iterations=3)
# dilation=cv2.dilate(binaria,kernel,iterations=3)
# cv2.imshow('Imagen',dilation)
# cv2.waitKey(0)


#EJ8
#-------EXTRAER PIXEL O PARTE DE LA IMAGEN--------
# imagen = cv2.imread('Logo.png')
# #extraer componentes R,G,B de un solo pixel
# (b,g,r) = imagen[269,514]
# print(f'R={r}, G={g}, B={b}')
# #Extraer region de interes (ROI)
# roi = imagen[125:480,840:1056]
# cv2.imshow('Imagen',roi)
# cv2.waitKey(0)


#EJ9
#-------REDIMENSIONAR UNA IMAGEN-------
# imagen = cv2.imread('Logo.png')
# (alto,ancho,canales) = imagen.shape
# print(f'Alto={alto}, Ancho={ancho}, canales={canales}')
# #redimensionamiento bruto
# redim = cv2.resize(imagen, (200,200))
# #redimensionamiento proporcional
# r = 300/ancho
# dim = (300, int(alto*r))
# redimp = cv2.resize(imagen,dim)
# cv2.imshow('Imagen',redimp)
# cv2.waitKey(0)


#EJ10
# #-----DIBUJAR OBJETOS Y TEXTO SOBRE IMAGENES----
# imagen = cv2.imread('Logo.png')

# #dibujar rectangulo
# img1 = imagen.copy()
# cv2.rectangle(img1, (874,338), (1018,376), (0,255,0),2)

# #dibujar circulo
# img2 = imagen.copy()
# cv2.circle(img2,(1235,307),140,(0,255,0),3)

# #dibujar linea
# img3 = imagen.copy()
# cv2.line(img3,(325,470),(512,470),(255,0,0),4)

# #dibujar texto
# img4 = imagen.copy()
# cv2.putText(img4,'OpenCV es bastante bueno',(800,100),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255))
# cv2.imshow('Imagen',img4)
# cv2.waitKey(0)


#EJ11
#------OPERACIONES MATEMATICAS ENTRE IMAGENES-------
#NOTA=operaciones con numpy se realizan normal, con opencv satura en 0 o 255
# imagen = cv2.imread('Logo.png')
# M = np.ones(imagen.shape,dtype='uint8')*100
# suma = cv2.add(imagen,M)
# resta = cv2.subtract(imagen, M)
# cv2.imshow('Imagen',resta)
# cv2.waitKey(0)


#EJ12
#----OPERACIONES LOGICAS Y MASCARAS----
# rectangulo = np.zeros((300,300),dtype='uint8')
# cv2.rectangle(rectangulo,(25,25),(275,275),255,-1)
# circulo = np.zeros((300,300),dtype='uint8')
# cv2.circle(circulo,(150,150),150,255,-1)

# opand = cv2.bitwise_and(rectangulo, circulo)
# opor  = cv2.bitwise_or(rectangulo, circulo)
# opxor = cv2.bitwise_xor(rectangulo, circulo)
# opnot = cv2.bitwise_not(rectangulo, circulo)
# cv2.imshow('Imagen',opand)
# cv2.waitKey(0)









