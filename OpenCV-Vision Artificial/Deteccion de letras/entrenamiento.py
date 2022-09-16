# -*- coding: utf-8 -*-
"""
Created on Tue Jun 21 22:42:55 2022

@author: CRISTIAN
"""

# import the necessary packages


from sklearn.model_selection import train_test_split
import numpy as np
import os
import cv2
import math
from sklearn.preprocessing import MinMaxScaler
import re
import matplotlib.pyplot as plt
from sklearn import svm, metrics
from sklearn.neural_network import MLPClassifier
from sklearn import tree

import tensorflow as tf
import imutils
from joblib import dump, load
from sklearn.ensemble import RandomForestClassifier

dirname = "D:/OPENCV/letras"
imgpath = dirname + "/"

images = []
directories = []
dircount = []
prevRoot=''
cant=0


def sacarmomentshu(imagen):
    huMoments = []
    image = cv2.imread(imagen)
    image = imutils.resize(image, width=1000, height=1800)
    gris = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    # Threshold image
    _,gris = cv2.threshold(gris, 100, 255, cv2.THRESH_BINARY_INV) 

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
    
    return momentshu



data = []
print("leyendo imagenes de ",imgpath)

for root, dirnames, filenames in os.walk(imgpath):
    for filename in filenames:
        if re.search("\.(jpg|jpeg|png|bmp|tiff)$", filename):
            cant=cant+1
            filepath = root+"/"+filename
            # image = plt.imread(filepath)
            # images.append(image)
            features = sacarmomentshu(filepath)
            data.append(features[0])
            b = "Leyendo..." + str(cant)
            print (b, end="\r")
            if prevRoot !=root:
                print(root, cant)
                prevRoot=root
                directories.append(root)
                dircount.append(cant)
                cant=0
dircount.append(cant)
dircount = dircount[1:]
dircount[0]=dircount[0]+1
print('Directorios leidos:',len(directories))
print("Imagenes en cada directorio", dircount)
print('suma Total de imagenes en subdirs:',sum(dircount))

    
#normalizo los momentos de Hu
min_max_scaler = MinMaxScaler() 
moments_hu = min_max_scaler.fit_transform(data)

labels=[]
indice=0
for cantidad in dircount:
    for i in range(cantidad):
        labels.append(indice)
    indice=indice+1
print("Cantidad etiquetas creadas: ",len(labels))

deportes=[]
indice=0
for directorio in directories:
    name = directorio.split(os.sep)
    print(indice , name[len(name)-1])
    deportes.append(name[len(name)-1])
    indice=indice+1

y = np.array(labels)
X = moments_hu #convierto de lista a numpy

# Find the unique numbers from the train labels
classes = np.unique(y)
nClasses = len(classes)
print('Total number of outputs : ', nClasses)
print('Output classes : ', classes)

#Mezclar todo y crear los grupos de entrenamiento y testing
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.20)


#Entrenamiento con maquina de soporte vectorial
clf = svm.SVC().fit(X_train, y_train) 

#Entrenamiento con perceptron multicapa
# clf = MLPClassifier(solver='lbfgs',max_iter=1000).fit(X_train, y_train)

#clf = RandomForestClassifier().fit(X_train, y_train)

#clf = tree.DecisionTreeClassifier().fit(X_train, y_train)

predicted = clf.predict(X_test)

print(
    f"Classification report for classifier {clf}:\n"
    f"{metrics.classification_report(y_test, predicted)}\n"
  )

print(clf.score(X_test, y_test))

# #Crear el modelo
# model = tf.keras.Sequential([
#   tf.keras.layers.Flatten(input_shape=(7,)),
#   tf.keras.layers.Dense(70, activation=tf.nn.relu),
#   tf.keras.layers.Dense(70, activation=tf.nn.relu),
#   tf.keras.layers.Dense(20, activation=tf.nn.softmax) #Para redes de clasificacion
# ])

# #Compilar el modelo
# model.compile(
#     optimizer='adam',
#     loss=tf.keras.losses.SparseCategoricalCrossentropy(),
#     metrics=['accuracy']
# )

# #Entrenar
# historial = model.fit(X_train,y_train,epochs=100,verbose=0)


# # evaluate the network
# print("[INFO] evaluating network...")
# predictions = model.predict(X_test)
# print(metrics.classification_report(y_test,
#  	predictions.argmax(axis=1)))

# scores = model.evaluate(X_train,  y_train)
# print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))



#GUARDAR MODELOS DE SKLEARN
#dump(clf, 'filename.joblib') 

# #GUARDAR MODELOS EN H5
# model.save('myModel2806222.h5')

