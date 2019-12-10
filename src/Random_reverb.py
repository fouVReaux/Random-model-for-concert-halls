#
#
#
#
#
#
import numpy as np
import scipy.io.wavfile
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

class RandomReverb():
    def __init__(self, volume, surface, alpha, ir_duration, fs):
        self.volume = volume
        self.surface = surface
        self.alpha = alpha
        self.fs = fs
        self.ir_duration = ir_duration
        #
        self.ADD_DIRECT_SOUND = 1
        self.DIST = np.random.poisson
        self.ir=0
        self.audioFilePath=""
        self.dataDry=0
    # --------------------------------------------------------------------------
    def set_direct_sound(self, val):
        self.ADD_DIRECT_SOUND=val
        return val

    def set_dist(self, dist):
        if dist == "poisson":
            self.DIST = np.random.poisson
            return 1

    def load_audio(self, audioFilePath):
        self.audioFilePath = audioFilePath
        fs, self.dataDry = scipy.io.wavfile.read(audioFilePath)
        return 0

    def normalized_audio(self, audioFilePath):
        #save a normalized version of the Input data sound
        factor = interp1d([self.dataDry.min(),self.dataDry.max()],[-0.7,0.7])
        noCov = self.dataDry
        scipy.io.wavfile.write(audioFilePath+"/input_normalized.wav", fs, factor(noCov))

    def convol_audio_ir(self, audioFilePath):
        convolution = np.convolve(self.dataDry, self.ir)*self.fs
        factor = interp1d([convolution.min(),convolution.max()],[-0.7,0.7])
        convOne = convolution
        scipy.io.wavfile.write(audioFilePath+"/conv_1.wav", fs, factor(convOne))
        return 0

    def comput_ir(self):
        # local var
        c = 340
        l = 4 * self.volume / self.surface
        Δt = 1 / self.fs
        λ = lambda t: (4 * np.pi * c**3 * t**2) / self.volume
        n = lambda t: c * t / l
        ir_len = self.ir_duration * self.fs

        # init of the ir
        ir = np.zeros((ir_len))
        # add the rirect sound or not
        if self.ADD_DIRECT_SOUND:
            ir[0] = 1
        # compute the reverb
        nb_arrivals_written = 0
        for i in range(ir_len):
            t = i * Δt
            nb_arrivals = self.DIST(λ(t), 1)[0]
            nb_arrivals_delta = (nb_arrivals - nb_arrivals_written)

            if nb_arrivals_delta > 1:
                nb_refls = 1 + self.DIST(n(t), 1)
                mag = (1 - self.alpha)**nb_refls
                ir[i] = mag * (-1) ** i
                nb_arrivals_written += 1

        self.ir = ir

    def save_ir(self):
        scipy.io.wavfile.write("ir.wav", self.fs, self.ir)

    def plot_ir(self):
        plt.plot(self.ir)
        plt.show()
        return 1

if __name__ == "__main__":
    # Room value
    volume = 2000       # m^3
    surface = volume/4  # m^2
    alpha = 0.4         # attenuation coefficient
    ir_duration = 1     # in seconds
    fs = 44100          # in Hz
    # Room simulation
    rr = RandomReverb(volume, surface, alpha, ir_duration, fs)
    rr.set_direct_sound(1)
    rr.set_dist("poisson")
    rr.comput_ir()
    rr.plot_ir()
    rr.load_audio("../sample/sample.wav")
    rr.normalized_audio("../sample")
    rr.convol_audio_ir("../sample")
