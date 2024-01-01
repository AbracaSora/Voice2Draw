import time
import urllib.request
import urllib.parse
import json
import hashlib
import base64
import config as cfg


class Segment:
    def __init__(self, segment: str):
        self.String = segment

    def KeyWords(self):
        body = urllib.parse.urlencode({'text': self.String}).encode('utf-8')
        param = {"type": "dependent"}
        x_param = base64.b64encode(json.dumps(param).replace(' ', '').encode('utf-8'))
        x_time = str(int(time.time()))
        x_checksum = hashlib.md5(cfg.NLP_API_KEY.encode('utf-8') + str(x_time).encode('utf-8') + x_param).hexdigest()
        x_header = {'X-Appid': cfg.NLP_APP_ID,
                    'X-CurTime': x_time,
                    'X-Param': x_param,
                    'X-CheckSum': x_checksum}
        req = urllib.request.Request(cfg.NLP_URL, body, x_header)
        result = urllib.request.urlopen(req)
        result = result.read()
        result = result.decode('utf-8')
        result = json.loads(result)
        keyword = []
        for i in result['data']['ke']:
            keyword.append(i['word'])
        return keyword
