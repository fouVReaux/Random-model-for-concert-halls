import librosa

inputfile="../sample/Melodie_1.wav"
outputfile="../sample/Melodie_1_rSR.wav"
outSr = 44100

y, sr = librosa.load(inputfile, sr=outSr)

librosa.output.write_wav(outputfile, y, sr, norm=False)
