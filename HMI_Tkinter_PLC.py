
# -*- coding: utf-8 -*-
"""
@author: CRISTIAN
"""

import snap7
from snap7.util import *
import tkinter as tk
from tkinter import ttk, messagebox

#Configuracion de la comunicacion
client = snap7.client.Client()
client.connect('192.168.0.1', 0, 1)
print(client.get_connected())

# def leer_entrada_digital():
#     dir_in_byte = 0
#     dir_in_bit = 0
#     lee_in=client.eb_read(dir_in_byte, 1)
#     W=get_bool(lee_in,0,dir_in_bit)
#     return W

def leer_entrada_analoga(entrada):
#Leer entrada analoga IW60
    lect2 = client.eb_read(entrada, 2)
    lect2 = get_int(lect2, 0)
    return lect2

def escalizar_entrada_analoga(entrada2):
    entrada_escalizada=(1000/27648)*entrada2
    print(f'Escalizacion del nivel {entrada_escalizada}')
    return entrada_escalizada

def activacion_ev1(entrada3):
    
    dir_in_byte = 0
    dir_in_bit = 0
    lee_in=client.eb_read(dir_in_byte, 1)
    I0_0 = get_bool(lee_in,0,dir_in_bit)
    
    if entrada3<=50:
        dir_sal_byte = 1
        dir_sal_bit = 0
        valor = 1
        lee_sal=client.ab_read(dir_sal_byte, 1)
        set_bool(lee_sal,0,dir_sal_bit,valor)
        w=client.ab_write(dir_sal_byte,lee_sal)
        return w
    
    
    elif entrada3>=950 or I0_0==True:
        dir_sal_byte = 1
        dir_sal_bit = 0
        valor = 0
        lee_sal=client.ab_read(dir_sal_byte, 1)
        set_bool(lee_sal,0,dir_sal_bit,valor)
        w=client.ab_write(dir_sal_byte,lee_sal)
        mensaje1='El nivel a superado el limite permitido'
        messagebox.showwarning('Mensaje Peligro', mensaje1)
        return w
    
def main():
    y1=leer_entrada_analoga(60)
    y=escalizar_entrada_analoga(y1)
    k=activacion_ev1(y)
    
    ventana = tk.Tk()
    ventana.geometry('600x400')
    ventana.title('Sistema nivel via snap7')
    ventana.iconbitmap('icono.ico')
    
    entrada1 = ttk.Entry(ventana, width=30)
    entrada1.grid(row=0, column=0)
    # Etiqueta (label)
    
    etiqueta1 = tk.Label(ventana, text='Forzar el sensor analogo de nivel')
    etiqueta1.grid(row=1, column=0, columnspan=2)
    
    etiqueta2 = tk.Label(ventana, text='Habilitar EV2')
    etiqueta2.grid(row=6, column=0, columnspan=2)
    
    
    etiqueta3 = tk.Label(ventana, text='Deshabilitar EV2')
    etiqueta3.grid(row=10, column=0, columnspan=2)
            
    #funciones para los botones
    
    def enviar():
        # Modificamos el texto del label
        #etiqueta1.config(text=entrada1.get())
        # Messagebox (cajas mensajes)
        mensaje1 = entrada1.get()
        #Escribir SALIDA entera IW60
        valor = set_int(bytearray(2), 0, mensaje1)
        client.eb_write(60, 2,valor)
        y1=leer_entrada_analoga(60)
        y=escalizar_entrada_analoga(y1)
        k=activacion_ev1(y)
    
    #EV1 Q0.0 EV2 Q0.1
        
    def enviar2():
        y1=leer_entrada_analoga(60)
        y=escalizar_entrada_analoga(y1)
        k=activacion_ev1(y)
        mensaje1='El deposito tiene menos de 75 litros'
        if y <= 75.0 :
            messagebox.showinfo('Mensaje Informativo', mensaje1)
    
        else:
        
            dir_sal_byte = 1
            dir_sal_bit = 1
            valor = 1
            lee_sal=client.ab_read(dir_sal_byte, 1)
            set_bool(lee_sal,0,dir_sal_bit,valor)
            client.ab_write(dir_sal_byte,lee_sal)
        
    def enviar3():
        #deshabilitar ev2
        dir_sal_byte = 1
        dir_sal_bit = 1
        valor = 0
        lee_sal=client.ab_read(dir_sal_byte, 1)
        set_bool(lee_sal,0,dir_sal_bit,valor)
        client.ab_write(dir_sal_byte,lee_sal)
    
    
    # Creamos un botón
    boton1 = ttk.Button(ventana, text='Enviar', command=enviar)
    boton1.grid(row=0, column=1)
    
    
    #crearemos un boton para habilitar la EV2
    boton2 = ttk.Button(ventana, text='Pulsar', command=enviar2)
    boton2.grid(row=6, column=1)
    
    #crearemos un boton para deshabilitar la EV2
    boton3 = ttk.Button(ventana, text='Pulsar', command=enviar3)
    boton3.grid(row=10, column=1)

    ventana.after(1000)  # run again after 1000ms (1s)
    
    ventana.after(1000) # run first time after 1000ms (1s)
    
    ventana.mainloop()
    
if __name__ == '__main__':
    main()

    



