# -*- coding: utf-8 -*-
"""
Created on Wed Jun  1 14:14:02 2016

@author: Paulo
"""
import matplotlib.pyplot as plt
import gtime
import pygame.draw
import gcolor

class guardaListas:
    
    def __init__(self):
        self.LISTATEMPO
        self.LISTADISTANCIA
    
#    def update():
            #calcula distancia atual entre os corpos
            #apende a lista tempo
        #quando lista tiver tamanho x, gera grafico
def grafico_pyplot(x,y):
    lista_tempo = []

    for tick in x:
            tempo = tick * gtime.RESOLUTION
            tempo = conversor_tempo_a(tempo)
            lista_tempo.append(tempo)
    
    plt.plot(lista_tempo,y)
    plt.show()



def grafico(x,y,screen,TIME_RESOLUTION = 1):
    pygame.draw.rect(screen, gcolor.Gcolor.BLUE, [1, 1, x, y])
        
        
def conversor_tempo_a(tempo): #converte para anos(por isso a)
    return ((((tempo/60)/60)/24)/365)