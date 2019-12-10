# Author: Olivier

import numpy as np
import scipy.io.wavfile
import matplotlib.pyplot as plt

ADD_DIRECT_SOUND = True
DIST = np.random.poisson

c = 340 # m.s^-1
# long = 15
# larg = 15
# haut = 5
# V = long*larg*haut # m^3
# S = 2*(long*larg+larg*haut+long*haut) # m^2
V = 2000
S = V / 4
α = 0.4
fs = 44100 # Hz
ir_duration = 1 # s
ir_len = ir_duration * fs

l = 4 * V / S

Δt = 1 / fs
λ = lambda t: (4 * np.pi * c**3 * t**2) / V
n = lambda t: c * t / l

ir = np.zeros((ir_len))
if ADD_DIRECT_SOUND:
    ir[0] = 1

nb_arrivals_written = 0
for i in range(ir_len):
    t = i * Δt
    nb_arrivals = DIST(λ(t), 1)[0]
    nb_arrivals_delta = (nb_arrivals - nb_arrivals_written)

    if nb_arrivals_delta > 1:
        nb_refls = 1 + DIST(n(t), 1)
        mag = (1 - α)**nb_refls
        ir[i] = mag * (-1) ** i
        nb_arrivals_written += 1

ir = ir / np.max(np.abs(ir)) * 0.9
scipy.io.wavfile.write("ir.wav", fs, ir)
plt.plot(ir)
plt.show()





