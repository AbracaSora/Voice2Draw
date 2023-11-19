import pickle
import numpy as np

from AudioRecorder import AudioRecorder
from keras.models import load_model


ar = AudioRecorder()
MusicModel = load_model('model/speech_mfcc_model.h5')
paradict = {}
with open('dataset/mfcc_model_para_dict.pkl', 'rb') as f:
    paradict = pickle.load(f)
DATA_MEAN = paradict['mean']
DATA_STD = paradict['std']
emotionDict = paradict['emotion']
edr = dict([(i, t) for t, i in emotionDict.items()])


def Emotion(path):
    ar.load(path)
    mfcc_data = ar.MFCC()
    feature = np.mean(mfcc_data, axis=0)
    feature = feature.reshape((313, 1))
    feature -= DATA_MEAN
    feature /= DATA_STD
    feature = feature.reshape((1, 313, 1))
    result = MusicModel.predict(feature)
    index = np.argmax(result, axis=1)[0]
    return edr[index]
