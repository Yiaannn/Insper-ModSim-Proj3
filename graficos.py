# -*- coding: utf-8 -*-
"""
Created on Wed Jun  1 14:14:02 2016

@author: Paulo
"""
import matplotlib.pyplot as plt
import gtime


def grafico_pyplot(x,y,TIME_RESOLUTION = 1):
    if x == -1:
        tempo = gtime.ticks * gtime.RESOLUTION
        tempo = conversor_tempo_a(tempo)
        
        plt.plot(tempo,y)
        plt.show
    else:
        
        plt.plot(x,y)
        plt.show


def grafico(x,y,TIME_RESOLUTION = 1):
    x = 0
        
        
def conversor_tempo_a(tempo): #converte para anos(por isso a)
    return ((((tempo/60)/60)/24)/365)