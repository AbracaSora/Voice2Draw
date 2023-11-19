import pyaudio as pa
import wave as wv


class Recorder:
    def __init__(self, channels=1, rate=16000, frames_per_buffer=1024):
        self.channels = channels
        self.rate = rate
        self.frames_per_buffer = frames_per_buffer
        self.p = pa.PyAudio()
        self.stream = None
        self.frames = []

    def open(self):
        self.stream = self.p.open(format=pa.paInt16,
                                  channels=self.channels,
                                  rate=self.rate,
                                  input=True,
                                  frames_per_buffer=self.frames_per_buffer)

    def read(self, path='testset/input.wav', seconds=5):
        print('recording...')
        wave_file = wv.open(path, 'wb')
        wave_file.setnchannels(self.channels)
        wave_file.setsampwidth(self.p.get_sample_size(pa.paInt16))
        wave_file.setframerate(self.rate)
        for i in range(0, int(self.rate / self.frames_per_buffer * seconds)):
            data = self.stream.read(self.frames_per_buffer)
            wave_file.writeframes(data)
        wave_file.close()
        print('done')

    def close(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
