import os
import pickle
import numpy as np

from AudioRecorder import AudioRecorder

ar = AudioRecorder()
counter = 0
fileDirCASIA = 'dataset'

MFCC = {'angry': [], 'fear': [], 'happy': [], 'neutral': [], 'sad': [], 'surprise': [], 'disgust': []}

listdir = os.listdir(fileDirCASIA)
for personDir in listdir:
    if r'.' not in personDir:
        emotionDirName = os.path.join(fileDirCASIA, personDir)
        emotionDir = os.listdir(emotionDirName)
        for ed in emotionDir:
            if r'.' not in ed:
                filesDirName = os.path.join(emotionDirName, ed)
                files = os.listdir(filesDirName)
                for fileName in files:
                    if fileName[-3:] == 'wav':
                        counter += 1
                        fn = os.path.join(filesDirName, fileName)
                        print(str(counter) + fn)
                        ar.load(fn)
                        mfcc_data = ar.MFCC()
                        feature = np.mean(mfcc_data, axis=0)
                        MFCC[ed].append(feature.tolist())

with open('dataset/mfcc_feature_dict.pkl', 'wb') as f:
    pickle.dump(MFCC, f)
