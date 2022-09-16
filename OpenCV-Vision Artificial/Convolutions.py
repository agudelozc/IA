from skimage.exposure import rescale_intensity
import numpy as np
import cv2

def convolucion(imagen, K):
    (iH, iW) = imagen.shape[:2]
    (kH, kW) = K.shape[:2]
    pad = (kW - 1) // 2
    imagen = cv2.copyMakeBorder(imagen, pad, pad, pad, pad, cv2.BORDER_REPLICATE)
    salida = np.zeros((iH, iW), dtype='float')
    for y in np.arange(pad, iH + pad):
        for x in np.arange(pad, iW + pad):
            roi = imagen[y - pad:y +  pad + 1, x - pad: x + pad + 1]
            k = (roi * K).sum()
            salida[y - pad, x - pad] = k
    salida = rescale_intensity(salida, in_range=(0,255))
    salida = (salida * 255).astype('uint8')
    return salida

#Definicion de filtros
smallBlur = np.ones((7, 7), dtype='float') * (1.0 / (7 * 7))
largeBlur = np.ones((21, 21), dtype='float') * (1.0 / (21 * 21))
sharpen = np.array(([0, -1, 0],
                   [-1, 5, -1],
                   [0, -1, 0]), dtype='int')
laplacian = np.array(([0, 1, 0],
                   [1, -4, 1],
                   [0, 1, 0]), dtype='int')
sobelX = np.array(([-1, 0, 1],
                   [-2, 0, 2],
                   [-1, 0, 1]), dtype='int')
sobelY = np.array(([-1, -2, -1],
                   [0, 0, 0],
                   [1, 2, 1]), dtype='int')
emboss = np.array(([-2, -1, 0],
                   [-1, 1, 1],
                   [0, 1, 2]), dtype='int')
kernelBank = (('small_blur', smallBlur),
              ('large_blur', largeBlur),
              ('sharpen', sharpen),
              ('laplacian', laplacian),
              ('sobel_x', sobelX),
              ('sobel_y', sobelY),
              ('emboss', emboss))

imagen = cv2.imread('IslaMujeres.jpg')
gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

for (Nombre, K) in kernelBank:
    print('Ejecutando {} Kernel'.format(Nombre))
    convol_man = convolucion(gris, K)
    convol_opencv = cv2.filter2D(gris, -1, K)
    cv2.imshow('Original', gris)
    cv2.imshow('Kernel {} Manual'.format(Nombre), convol_man)
    cv2.imshow('Kernel {} OpenCV'.format(Nombre), convol_opencv)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


