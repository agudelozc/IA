# -*- coding: utf-8 -*-
"""
@author: CRISTIAN 
"""
import time
import serial
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import skfuzzy as fz
uart = serial.Serial('/dev/ttyACM2',115200)  #config serial

flg_ctl = 'k' #cmd control
flg_ctl=str.encode(flg_ctl)
flg_ctl2='t'
flg_ctl2=str.encode(flg_ctl2)
R = 4.88 #resolución del ADC
Ks = 10.0 #factor escala LM35


U=np.arange(-45,51,1)

#funciones de pertenencia del error
etne=fz.trapmf(U,[-45,-45,-4,0])
etze=fz.trimf(U,[-4,0,4])
etpo=fz.trapmf(U,[0,4,50,50])




#DERIVADA

D=np.arange(-4,5,1)
detmn= fz.trapmf(D,[-4,-4,-2,-1])
detne= fz.trimf(D,[-2,-1,0])
detze= fz.trimf(D,[-1,0,1])
detpo= fz.trimf(D,[0,1,2])
detmp= fz.trapmf(D,[1,2,4,4])


V=np.arange(0,5.01,0.01)

DCmbj=fz.trapmf(V,[0,0,1,2])
DCbj=fz.trimf(V,[1,2,2.5])
DCmdo=fz.trimf(V,[2,2.5,3])
DCalt=fz.trimf(V,[2.5,3,3.5])
DCmat=fz.trapmf(V,[3,3.5,5,5])


muestras=int(input('Introduzca cantidad de muestras: '))

x_n=pd.DataFrame(columns=['Tiempo','Temperatura'])

temp1=np.array([])
time1=np.array([])


r = float(input('Ingrese referencia de temperatura (35 a 75): '))

#dependiendo del numero de muestras me grafica la cantidad
#de datos de temperatura
ejes= plt.gca() #creacion de ejes	
ejes.grid()  #rejilla
ejes.set_xlim(0,muestras) #Limite en x
ejes.set_xlabel('Tiempo')  #titulo eje x
ejes.set_ylim(0,100) # limite en y
ejes.set_ylabel('Temperatura °C') #titulo eje y
line ,= ejes.plot(x_n.Tiempo,x_n.Temperatura,'r') #plotea las 2 estructuras


for i in range(abs(muestras)):
        uart.write(flg_ctl) #envía cmd
        vr_ascii = uart.readline()
        cod_num = int(vr_ascii)
        Tm = (R * cod_num)/Ks
        TA=format(Tm,".2f")
        x_n.loc[i,'Tiempo']=i #nuevo instante de muestreo
        x_n.loc[i,'Temperatura']=Tm #nueva muestra

        e = r - Tm
        #Funciones de pertenencia para VL 1 e(t)
        u_etne = fz.interp_membership(U,etne,e)
        u_etze = fz.interp_membership(U,etze,e)
        u_etpo = fz.interp_membership(U,etpo,e)
        valor=np.array([u_etne,u_etze,u_etpo])
        a=valor.sum()
        b=format(a,".2f")
        #print(f"Ref={r}, Tm={TA} , Ruspini del error ={b}\n")

        temp1=np.append(temp1,x_n.at[i,'Temperatura'])
        time1=np.append(time1,x_n.at[i,'Tiempo'])
        
        m=(temp1[i]-temp1[i-1])/(time1[i]-time1[i-1])
        #m=np.diff(temp1)/np.diff(time1)
        
        
        #Funciones de pertenencia para VL 2 de(t)/dt
        u_detmn = fz.interp_membership(D,detmn,m)
        u_detne = fz.interp_membership(D,detne,m)
        u_detze = fz.interp_membership(D,detze,m)
        u_detpo = fz.interp_membership(D,detpo,m)
        u_detmp = fz.interp_membership(D,detmp,m)
        
        valor2=np.array([u_detmn,u_detne,u_detze,u_detpo,u_detmp])
        y=valor2.sum()
        x=format(y,".2f")
        # print ('x[',i,']: ')
        print(f"x[{i}]: Ref={r}, Tm={TA} , RP_error ={b}, RP_de/dt ={x} ")

        
        #Implicacion de 2 reglas con el conjunto minimo
        R1= np.fmin(u_etne,u_detmn)
        imp_R1=np.fmin(R1,DCmbj)
        
        R2 = np.fmin(u_etne,u_detne)
        imp_R2 = np.fmin(R2,DCmbj)
        
        R3 = np.fmin(u_etne,u_detze)
        imp_R3 = np.fmin(R3,DCmbj)
        
        R4= np.fmin(u_etne,u_detpo)
        imp_R4 = np.fmin(R4,DCmbj)
        
        R5= np.fmin(u_etne,u_detmp)
        imp_R5 = np.fmin(R5,DCbj)
        
        R6= np.fmin(u_etze,u_detmn)
        imp_R6 = np.fmin(R6,DCbj)
        
        R7= np.fmin(u_etze,u_detne)
        imp_R7 = np.fmin(R7,DCbj)
        
        R8 = np.fmin(u_etze,u_detze)
        imp_R8= np.fmin(R8,DCmdo)
        
        R9 = np.fmin(u_etze,u_detpo)
        imp_R9 = np.fmin(R9,DCmdo)
        
        R10 = np.fmin(u_etze,u_detmp)
        imp_R10 = np.fmin(R10,DCmdo)
        
        R11= np.fmin(u_etpo,u_detmn)
        imp_R11 = np.fmin(R11,DCmdo)
        
        R12 = np.fmin(u_etpo,u_detne)
        imp_R12 = np.fmin(R12,DCalt)
        
        R13 = np.fmin(u_etpo,u_detze)
        imp_R13= np.fmin(R13,DCalt)
        
        R14= np.fmin(u_etpo,u_detpo)
        imp_R14 = np.fmin(R14,DCalt)
        
        R15 = np.fmin(u_etpo,u_detmp)
        imp_R15 = np.fmin(R15,DCmat)
        
        #Agregacion de las reglas con el conjunto maximo
        agre_1=np.fmax(imp_R1,imp_R2)
        agre_2=np.fmax(agre_1,imp_R3)
        agre_3=np.fmax(agre_2,imp_R4)
        agre_4=np.fmax(agre_3,imp_R5)
        agre_5=np.fmax(agre_4,imp_R6)
        agre_6=np.fmax(agre_5,imp_R7)
        agre_7=np.fmax(agre_6,imp_R8)
        agre_8=np.fmax(agre_7,imp_R9)
        agre_9=np.fmax(agre_8,imp_R10)
        agre_10=np.fmax(agre_9,imp_R11)
        agre_11=np.fmax(agre_10,imp_R12)
        agre_12=np.fmax(agre_11,imp_R13)
        agre_13=np.fmax(agre_12,imp_R14)
        agre_14=np.fmax(agre_13,imp_R15)
        
        DCOUT=agre_14
        cog=fz.defuzz(V,DCOUT,'centroid')
        
        uart.write(flg_ctl2) #envía cmd
        uart.write(cog)
        
        
        print(f"PWM ES: {cog} ,el error es {e} ,la derivada es {m}")
        # singleton_cog = fz.interp_membership(V,DCOUT,cog)

        line.set_xdata(x_n.Tiempo)
        line.set_ydata(x_n.Temperatura)
        plt.draw() #Actualiza la figura
        plt.pause(1e-17) #pausa en segundos la grafica
        time.sleep(1.0) #periodo de muestreo
print('Fin')
        
