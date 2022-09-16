# import the opencv library
import cv2
import math
from joblib import dump, load
import numpy as np
from sklearn.preprocessing import MinMaxScaler



# define a video capture object
vid = cv2.VideoCapture(0)
while(True):
      
    # Capture the video frame
    # by frame
    ret, frame = vid.read()
    #Procesar
    # (B, G, R) = cv2.split(frame)
    # binaria = cv2.inRange(B, 50, 255)
    # binaria = cv2.bitwise_not(binaria)
    gris = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    # Threshold image
    _,gris = cv2.threshold(gris, 155, 255, cv2.THRESH_BINARY_INV)
    # #suavizar la imagen con un filtrado gaussiano
    gaussiana = cv2.GaussianBlur(gris, (3,3), 0)
    # Calculate Moments
    moments = cv2.moments(gaussiana)
    # Calculate Hu Moments
    huMoments = cv2.HuMoments(moments)
    hu=np.array([])
    # Log scale hu moments
    contours, hierarchy = cv2.findContours(gris, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for i in contours:
         area = cv2.contourArea(i)
         if area > 1000:
             x,y,w,h = cv2.boundingRect(i)
             cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 3)
             # Log scale hu moments
             for i in range(0,7):
                 huMoments[i] = (-1* math.copysign(1.0, huMoments[i]) * math.log10(abs(huMoments[i])))
                 hu = huMoments.T

    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
  
# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()


# EigenFaces
# if result[1] < 5700:
#     cv2.putText(frame,'{}'.format(imagePaths[result[0]]),(x,y-25),2,1.1,(0,255,0),1,cv2.LINE_AA)
#     cv2.rectangle(frame, (x,y),(x+w,y+h),(0,255,0),2)
# else:
#     cv2.putText(frame,'Desconocido',(x,y-20),2,0.8,(0,0,255),1,cv2.LINE_AA)
#     cv2.rectangle(frame, (x,y),(x+w,y+h),(0,0,255),2)