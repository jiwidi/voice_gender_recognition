import tensorflow as tf
import tarfile
import numpy as np
import pandas as pd
import re
import time
import python_speech_features as psf
import scipy.io.wavfile as wav
import os
masterList=[]
dir='/Users/jiwidi/Documents/Github/Sandvik/rawData/'
wavNumber=0
df=pd.DataFrame()
for file in os.listdir(dir):
    #for file in filelist
    if '.tgz' in file:
        print("Opening{0}".format(file))
        tar = tarfile.open(dir+file,'r:gz')
        tempWavList=[]
        #tar.extractall()
        for member in tar.getmembers():
            #Preprocess audio singal and extract all variables psf allow us
            if ".wav" in member.name:
                head, tail = os.path.split(member.name)
                f = tar.extract(member,"tmp/")
                #Put make dir
                os.rename("tmp/"+member.name, "audios/audio{0}.wav".format(wavNumber))

                wavNumber+=1
                #rate, audioFile = wav.read(tar.extractfile(member))
                #audioFeatures = psf.mfcc(audioFile, rate, 0.025, 0.01, 20, appendEnergy = True)
                tempWavList.append("audio{0}.wav".format(wavNumber))
            #Get the extra variables from the readme
            elif "README" in member.name:
                f = tar.extractfile(member)
                if f:
                    for line in f.readlines():
                        line=str(line)
                        if("User Name" in line):
                            user = re.split(":| ",line)[-1][:-3]
                            user = ''.join(e for e in user if e.isalnum())
                        elif("Age Range"in line):
                            age = re.split(":| ",line)[-1][:-3]
                            age = ''.join(e for e in age if e.isalnum())
                        elif("Gender"in line):
                            gender = 'female' if ('female' in line.lower()) else( 'male' if ('male' in line.lower()) else float('nan') )
                        elif("Language"in line):
                            language = re.split(":| ",line)[-1][:-3]
                            language = ''.join(e for e in language if e.isalnum())

                        elif("dialect"in line):
                            aux = re.split(":| ",line)[-2:]
                            aux[0] = ''.join(e for e in aux[0] if e.isalnum())
                            aux[1] = ''.join(e for e in aux[1] if e.isalnum())
                            dialect = aux[0] + aux[1]
                        elif("File type"in line):
                            fileType = re.split(":| ",line)[-1][:-3]
                            fileType = ''.join(e for e in fileType if e.isalnum())
                        elif("Sampling Rate"in line):
                            rate = re.split(":| ",line)[-1][:-3]
                            rate = ''.join(e for e in rate if e.isalnum())
                        elif("Sample rate"in line):
                            rateFormat = re.split(":| ",line)[-1][:-3]
                            rateFormat = ''.join(e for e in rateFormat if e.isalnum())
                        elif("channels"in line):
                            channels = re.split(":| ",line)[-1][:-3]
                            channels = ''.join(e for e in channels if e.isalnum())


        for idx, audioName in enumerate(tempWavList):
            masterList.append([audioName,user,age, gender, language,dialect,fileType,rate,rateFormat,channels])



headers=["sound.files","user","age","gender","language","dialect","fileType","rate","rateFormat","channels"]

df=pd.DataFrame(masterList,columns=headers)
df.to_csv('~/Documents/Github/Sandvik/wavDataset.csv',index=False)
print("Done")
