import config as cfg
import aip

Speech = aip.AipSpeech(cfg.SPEECH_APP_ID, cfg.SPEECH_API_KEY, cfg.SPEECH_SECRET_KEY)


class ASR:
    def __init__(self, audio_file):
        self.audio_file = audio_file
        with open(audio_file, 'rb') as fp:
            self.audio_data = fp.read()

    def translate(self):
        res = Speech.asr(self.audio_data, 'wav', 16000, {
            'dev_pid': 1537,
        })
        if res['err_no'] == 0:
            return res['result'][0]
        else:
            return None
