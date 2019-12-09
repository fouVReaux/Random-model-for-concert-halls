import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.interpolate import interp1d

def main():
    #samplerate
    Fs = 44100
    #file path
    pathDrySample = "sample/sample.wav";
    pathIR = "sample/ir.wav";
    pathConvolutionOutput = "sample/convolutions/";
    numberOfPass = 10

    fs, dataDry = wavfile.read(pathDrySample)
    fs, dataIR = wavfile.read(pathIR)

    print("---------------------------") 
    print('START  Convolution 0 : original')
    factor = interp1d([dataDry.min(),dataDry.max()],[-0.7,0.7])
    noCov = dataDry
    wavfile.write(pathConvolutionOutput+"conv_0.wav", fs, factor(noCov))
    print('FINISH Convolution 0')
    print("---------------------------") 
    print('START  Convolution 1')
    convolution = np.convolve(dataDry, dataIR)*fs
    factor = interp1d([convolution.min(),convolution.max()],[-0.7,0.7])
    convOne = convolution
    wavfile.write(pathConvolutionOutput+"conv_1.wav", fs, factor(convOne))
    print('FINISH Convolution 1')
    print("---------------------------")    

    for n in range(2,numberOfPass+1):
        print("START  Convolution "+str(n))
        convolutionN = np.convolve(convolution, dataIR)*fs
        factor = interp1d([convolutionN.min(),convolutionN.max()],[-1,1])
        convolution = convolutionN
        wavfile.write(pathConvolutionOutput+"conv_"+str(n)+".wav", fs, factor(convolutionN))
        print("FINISH Convolution "+str(n))
        print("---------------------------")

        
if __name__ == "__main__":
    main()
