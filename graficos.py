# -*- coding: utf-8 -*-
"""
Created on Wed Jun  1 14:14:02 2016

@author: Paulo
"""
import matplotlib.pyplot as plt


def grafico(ticks,y,TIME_RESOLUTION = 1):
    tempo = ticks * TIME_RESOLUTION
    tempo = conversor_tempo_a(tempo)
    
    plt.plot(tempo,y)
    plt.show
    
def conversor_tempo_a(tempo): #converte para anos(por isso a)
    return ((((tempo/60)/60)/24)/365)