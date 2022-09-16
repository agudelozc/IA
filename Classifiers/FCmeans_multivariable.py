# -*- coding: utf-8 -*-
"""
Created on Fri Apr 22 10:47:29 2022

@author: CRISTIAN
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import csv
from fcmeans import FCM

#datos sin normalizar
data = np.genfromtxt(r'D:\CONTROL INTELIGENTE-2\base_multi.csv', delimiter=',')
t=np.arange(1,1632,1)

# plt.plot(t,data[:,0],t,data[:,1],t,data[:,2],t,data[:,3])
# plt.title('Adquisicion de datos modulo multivariable')
# plt.xlabel('Tiempo [s]')
# plt.ylabel('Salida/Escalones %')

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

#para ordenar la base de datos en un array de 4 columnas con los datos 
#normalizados
#datos=np.array([normsp,normy,data[:,2],normq]).transpose()
datos=np.array([normsp,normy,normq]).transpose()
#Uso del clasificador FCMeans
fcm = FCM(n_clusters=14,m=1.5)
fcm.fit(datos)

# centroids
fcm_centers = fcm.centers
#Predicion de los datos entrenados con los mismos datos
fcm_labels = fcm.predict(datos)


#Creo una lista correspondiente a 10 colores que me van a identificar cada clase
colores=['blue','green','red','cyan','magenta','yellow','black','white','orange','brown']
asignar=[]
#un ciclo for para que a cada dato que se le hizo la prediccion le asigne un color
# for row in fcm_labels:
#      asignar.append(colores[row])
    
# #Se crea un arreglo para añadir las diferentes clases que se predijo
labels2=np.array(fcm_labels)#graficacion de las clases 
plt.figure(figsize=(20,5))
labels2=np.array(fcm_labels)
plt.plot(t,labels2)

# #Graficiacion de la base de datos con su parte clasificada
# plt.figure(figsize=(20,5))
# plt.scatter(t,datos[:,0],c=asignar,s=30)
# plt.scatter(t,datos[:,1],c=asignar,s=30)
# plt.scatter(t,datos[:,2],c=asignar,s=30)
# #plt.scatter(t,datos[:,3],c=asignar,s=30)

plt.figure(figsize=(20,5))
grados_pertenencia=fcm.u
plt.plot(grados_pertenencia)