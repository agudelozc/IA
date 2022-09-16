# -*- coding: utf-8 -*-
"""
Created on Mon Jul 11 17:58:04 2022

@author: CRISTIAN
"""
#importacion de librerias
from sklearn.cluster import DBSCAN
import numpy as np
import matplotlib.pyplot as plt
import csv
import pandas as pd

#INICIO DEL PROGRAMA

#Se crea un vector tiempo para graficar
t=np.arange(1,1631,1)

#datos sin normalizar
df =  pd.read_excel('base.xlsx')

data=np.array(df)
#graficacion de la base de datos
plt.figure(figsize=(20,5))
plt.plot(t,data[:,0],t,data[:,1],t,data[:,2])
plt.title('Adquisicion de datos modulo multivariable')
plt.xlabel('Tiempo [s]')
plt.ylabel('Salida/Escalones %')

#Tratamiento de datos para normalizar la base de datos
spmax=max(data[:,0]) #maximo valor del setpoint
spmin=min(data[:,0]) #minimo valor del setpoint
ymax=max(data[:,1])#maximo valor de la salida "controlada"
ymin=min(data[:,1])#minimo valor de la salida "controlada"
qmax=max(data[:,3])#maximo valor de la variable caudal
qmin=min(data[:,3])#minimo valor de la variable caudal

#normalizacion de datos para que esten en rango de 0-1
#Creo unas listas donde se van a almacenar los datos normalizados
normsp=[]
normy=[]
normq=[]
z=len(data[:,0])
for i in range(z):
    nsp=(data[:,0][i]-spmin)/(spmax-spmin)
    normsp.append(nsp)
    
    ny=(data[:,1][i]-ymin)/(ymax-ymin)
    normy.append(ny)
    
    nq=(data[:,3][i]-qmin)/(qmax-qmin)
    normq.append(nq)

plt.figure(figsize=(20,5))
#graficacion de datos normalizados
plt.plot(t,normsp,t,normy,t,data[:,2],t,normq)
plt.title('Graficacion datos normalizados')

#para ordenar la base de datos en un array de 4 columnas con los datos 
#normalizados
datos=np.array([normsp,normy,data[:,2]]).transpose()

clf = DBSCAN(eps=0.1).fit(datos)

#Predicion de los datos entrenados con los mismos datos
labels= clf.labels_
plt.figure(figsize=(20,5))
plt.plot(t,labels)
plt.title('Clases encontradas')
