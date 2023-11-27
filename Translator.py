import requests
import random
import json
import config as cfg
from hashlib import md5


class Translator:
    def __init__(self, from_lang='zh', to_lang='en'):
        self.from_lang = from_lang
        self.to_lang = to_lang

    def translate(self, query=None):
        if query is '':
            return ''
        salt = random.randint(32768, 65536)
        sign = md5((cfg.TRANS_APPID + query + str(salt) + cfg.TRANS_APIKEY).encode("utf-8")).hexdigest()

        # Build request
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        payload = {'appid': cfg.TRANS_APPID, 'q': query, 'from': self.from_lang, 'to': self.to_lang, 'salt': salt, 'sign': sign}

        # Send request
        r = requests.post(cfg.TRANS_URL, params=payload, headers=headers)
        result = r.json()

        # Show response
        return result['trans_result'][0]['dst']
        # For list of language codes, please refer to `https://api.fanyi.baidu.com/doc/21`
