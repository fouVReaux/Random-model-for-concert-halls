# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 11:04:57 2019

@author: Hugo
"""
import numpy as np
import scipy.signal as signal
import soundfile as sf

Fe = 44100
V = 2107
S = 801
l = 4*V/S
c = 340
alpha = 0.3
duree = int(2*((0.16*V)/(alpha*S))*Fe)
t = np.linspace(0,duree/Fe,duree)

#data,fs = sf.read('melodie_stereo.wav')
h = np.zeros(len(t))

for k in range( len(t) ):
    nMoy = (c*t[k])/l
    n = np.random.poisson(nMoy,1)
    I = (1-alpha)**n
    h[k] = h[k] + I

sf.write('ir.wav', h, 44100)
