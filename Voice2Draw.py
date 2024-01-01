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
        self.translatedString = ''
        self.keywords = []
        self.emotion = ''
        self.prompt = ''
        self.image = None
        self.seed = seed
        self.name = name
        self.size = size
        self.steps = steps
        self.mode = 'text'

    def setSize(self, size):
        self.size = size

    def setPath(self, path):
        self.path = path

    def appendKeywords(self, keywords):
        self.keywords.append(keywords)

    def generatePrompt(self):
        self.prompt = ''
        for words in self.keywords:
            self.prompt += words.strip()
            self.prompt += ','
        self.prompt += self.translatedString.strip()

    def input(self, rawString):
        self.rawString = rawString
        self.translatedString = Translator('zh', 'en').translate(self.rawString).strip()

    def readWave(self):
        r = Recorder()
        r.open()
        r.read(self.path)
        r.close()
        self.emotion = Emotion(self.path)

    def readWaveFromFile(self, path):
        self.path = path
        self.input(ASR(self.path).translate())
        self.emotion = Emotion(self.path)

    def setSeed(self, seed):
        self.seed = seed

    def setImageName(self, name):
        self.name = name

    def generateImage(self):
        if self.mode == 'text':
            self.image, self.seed = ImageGenerator(self.size, self.steps).TextGenerate(self.prompt,
                                                                                       emotion=self.emotion,
                                                                                       name=self.name,
                                                                                       seed=self.seed)
        elif self.mode == 'image':
            self.image, self.seed = ImageGenerator(self.size, self.steps).ImageGenerate(self.prompt,
                                                                                        emotion=self.emotion,
                                                                                        name=self.name,
                                                                                        seed=self.seed,
                                                                                        image=self.image)

    def clear(self):
        self.prompt = ''
        self.keywords = []
