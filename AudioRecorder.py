import librosa
import librosa.feature
import matplotlib.pyplot as plt
import numpy as np


def normalizeVoiceLen(y, normalizedLen):
    nFrames = len(y)
    y = np.reshape(y, [nFrames, 1]).T
    # 归一化音频长度为2s,80000数据点
    if nFrames < normalizedLen:
        res = normalizedLen - nFrames
        res_data = np.zeros([1, res], dtype=np.float32)
        y = np.reshape(y, [nFrames, 1]).T
        y = np.c_[y, res_data]
    else:
        y = y[:, 0:normalizedLen]
    return y[0]


def getNearestLen(frameLength, sr):
    frameSize = frameLength * sr
    # 找到与当前framesize最接近的2的正整数次方
    nfftDict = {}
    lists = [32, 64, 128, 256, 512, 1024]
    for i in lists:
        nfftDict[i] = abs(frameSize - i)
    sortList = sorted(nfftDict.items(), key=lambda x: x[1])  # 按与当前framesize差值升序排列
    frameSize = int(sortList[0][0])  # 取最接近当前framesize的那个2的正整数次方值为新的framesize
    return frameSize


class AudioRecorder:

    def __init__(self):
        self.y = None
        self.sr = None
        self.n_fft = None
        self.mfcc_data = None

    def load(self, path: str):
        self.y, self.sr = librosa.load(path, sr=None)
        self.n_fft = getNearestLen(0.25, self.sr)
        self.y = normalizeVoiceLen(self.y, 80000)

    def MFCC(self):
        # 提取mfcc特征
        self.mfcc_data = librosa.feature.mfcc(y=self.y, sr=self.sr, n_mfcc=13, n_fft=self.n_fft,
                                              hop_length=int(self.n_fft / 4))
        return self.mfcc_data
