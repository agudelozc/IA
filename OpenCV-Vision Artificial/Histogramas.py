import cv2
import numpy as np
from matplotlib import pyplot as plt

#Histograma a imagen en escala de grises
imagen = cv2.imread('RojoVerdeMorado.png')
gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
hist = cv2.calcHist(gris, [0], None, [256], [0, 256])
plt.figure()
plt.title('Histograma escala de grises')
plt.xlabel('Bits')
plt.ylabel('# de pixeles')
plt.plot(hist)
plt.xlim([0, 256])
#plt.show()
#cv2.waitKey(0)

#Histograma de imagenes a color
canales = cv2.split(imagen)
colores = ('b', 'g', 'r')
plt.figure()
plt.title('Histograma de colores')
plt.xlabel('Bits')
plt.ylabel('# de pixeles')
for (canal, color) in zip(canales, colores):
    hist = cv2.calcHist([canal], [0], None, [256], [0, 256])
    plt.plot(hist, color = color)
    plt.xlim([0, 256])
plt.show()
cv2.waitKey(0)

Nombre = 'Santiago'
Apellido = 'Barrera'
print(Nombre)
print('Mi nombre es: ', Nombre)
print("Mi nombre es {}, y mi apellido es {}".format(Nombre,Apellido))
print(f'Mi nombre es {Nombre}, y mi apellido es {Apellido}')
