# -*- coding: utf-8 -*-
"""
Created on Thu Jul 21 16:29:32 2022

@author: CRISTIAN
"""

#Importacion de librerias a utilizar
from sklearn.model_selection import train_test_split
import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm, metrics
import pandas as pd


t = np.arange(1,1631,1)
df = pd.read_excel('base.xlsx')

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
plt.legend(["Setpoint", 'Salida Y','LeyControl','Caudal'], loc ="best")

#tratamiento de los datos variables y target
X= np.array([normsp,normy,data[:,2],normq]).T #variables a entrenar 
y=data[:,4] #clases


# Find the unique numbers from the train labels
classes = np.unique(y)
nClasses = len(classes)
print('Total number of outputs : ', nClasses)
print('Output classes : ', classes)

#Mezclar todo y crear los grupos de entrenamiento y testing
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.20)

#graficacion de clases originales
plt.figure(figsize=(20,5))
plt.plot(y)
plt.title('Figura original de clases')

#graficacion de clases a testear o registros temporales
plt.figure(figsize=(20,5))
plt.plot(y_test)
plt.title('Figura de registros temporales de clases')

#Entrenamiento con maquina de soporte vectorial
clf = svm.SVC(C=5).fit(X_train, y_train) 

#prediccion con los datos aleatorios seleccionados de X
predicted = clf.predict(X_test)

print(
    f"Classification report for classifier {clf}:\n"
    f"{metrics.classification_report(y_test, predicted)}\n"
  )

print(f'Precisión {round(clf.score(X_test, y_test),4)} %')
plt.figure(figsize=(20,5))
plt.plot(y_test,'--',predicted,'*')
plt.title('Clases seleccionadas vs clases de prediccion')