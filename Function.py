from Voice2Draw import Voice2Draw
from Translator import Translator

trans = Translator('zh', 'en')
v2d = Voice2Draw()


def ReadWave(path='testset/input.wav'):
    v2d.setPath(path)
    v2d.readWave()


def ReadWaveFromFile(path):
    v2d.readWaveFromFile(path)


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
    return v2d.image


def ImageChange():
    v2d.generatePrompt()
    v2d.changeImage()
    return v2d.image
