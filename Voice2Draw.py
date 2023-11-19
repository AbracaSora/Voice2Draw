from Segment import Segment
from ImageGenerator import ImageGenerator
from Recorder import Recorder
from Emotion import Emotion
from ASR import ASR
from Translator import Translator


class Voice2Draw:
    def __init__(self, segment: str = '', name='untitled', seed=-1, size=(1024, 1024), steps=120,
                 path='testset/input.wav'):
        self.path = path
        self.rawString = Segment(segment)
        self.keywords = []
        self.emotion = ''
        self.prompt = ''
        self.image = None
        self.seed = seed
        self.name = name
        self.size = size
        self.steps = steps

    def setSize(self, size):
        self.size = size

    def setPath(self, path):
        self.path = path

    def appendKeywords(self, keywords):
        self.keywords.append(keywords)

    def generatePrompt(self):
        for words in self.keywords:
            self.prompt += words.strip()
            self.prompt += ','

    def input(self, emotion, rawString):
        self.emotion = emotion
        self.rawString = rawString
        self.keywords.append(Translator('zh', 'en').translate(self.rawString).strip())

    def readWave(self):
        r = Recorder()
        r.open()
        r.read(self.path)
        r.close()
        self.input(Emotion(self.path), ASR(self.path).translate())

    def readWaveFromFile(self, path):
        self.path = path
        self.input(Emotion(self.path), ASR(self.path).translate())

    def setSeed(self, seed):
        self.seed = seed

    def setImageName(self, name):
        self.name = name

    def generateImage(self):
        self.image, self.seed = ImageGenerator(self.size, self.steps).TextGenerate(self.prompt, emotion=self.emotion,
                                                                                   name=self.name,
                                                                                   seed=-1)

    def changeImage(self):
        self.image, self.seed = ImageGenerator(self.size, self.steps).TextGenerate(self.prompt, emotion=self.emotion,
                                                                                   name=self.name,
                                                                                   seed=self.seed)
