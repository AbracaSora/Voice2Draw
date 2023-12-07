import base64

from Voice2Draw import Voice2Draw
from Translator import Translator
from PyQt5.QtCore import QObject, pyqtSignal

Dict = {
    '开心': 'happy',
    '平静': 'peace',
    '愤怒': 'angry',
    '悲伤': 'sad',
    '惊喜': 'surprise',
    '恐惧': 'fear',
    '水彩': '(((ink))), ((watercolor))',
    '铅笔速写': '(monochrome), (gray scale), (pencil sketch lines)',
    '剪影(推荐人像)': '(silhouette)',
    '暖色调': '(warm colors)',
    '冷色调': '(cold colors)',
    '中间色': '(middle colors)',
}


class RecordEndSignal(QObject):
    recordEnd = pyqtSignal(str)


class GenerateEndSignal(QObject):
    generateEnd = pyqtSignal(str)


class AnalyzeEndSignal(QObject):
    analyzeEnd = pyqtSignal(str)


recordEndSignal = RecordEndSignal()
generateEndSignal = GenerateEndSignal()
analyzeEndSignal = AnalyzeEndSignal()

trans = Translator('zh', 'en')
v2d = Voice2Draw(size=(610, 610), steps=120)


def ReadWave(path='testset/input.wav'):
    v2d.setPath(path)
    v2d.readWave()
    recordEndSignal.recordEnd.emit("RecordEnd")


def ReadWaveFromFile(path='testset/input.wav'):
    v2d.readWaveFromFile(path)
    analyzeEndSignal.analyzeEnd.emit("AnalyzeEnd")


def SetSize(size):
    v2d.setSize(size)


def EmotionSelect(emotion: str):
    v2d.appendKeywords(emotion)


def StyleSelect(style: str):
    v2d.appendKeywords(style)


def ExtraKeywords(keywords: str):
    arr = keywords.split(',')
    for word in arr:
        word = trans.translate(word)
        v2d.appendKeywords(word.strip())


def ImageGenerate():
    v2d.generatePrompt()
    v2d.generateImage()
    # generateEndSignal.generateEnd.emit(v2d.image)
    generateEndSignal.generateEnd.emit("GenerateEnd")
    return v2d.image


def ImageChange():
    v2d.generatePrompt()
    v2d.changeImage()
    return v2d.image


def DataAnalysis(data: dict):
    if data['emotion'] != '自动识别':
        v2d.appendKeywords(Dict[data['emotion']])
    else:
        v2d.appendKeywords(v2d.emotion)
    if data['style'] != '默认':
        v2d.appendKeywords(Dict[data['style']])
    if data['tone'] != '默认':
        v2d.appendKeywords(Dict[data['tone']])
    if data['prop'] == '1:1' or data['prop'] == '默认':
        v2d.setSize((620, 620))


def SaveImage(Path: str):
    with open(Path, 'wb') as image_file:
        image_file.write(base64.b64decode(v2d.image))
