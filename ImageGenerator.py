import json
import base64
import requests
import config as cfg


def _submit_post(url: str, Data: dict):
    return requests.post(url, data=json.dumps(Data))


class ImageGenerator:

    def __init__(self, size: tuple, steps: int, url=cfg.SD_WEB_URL):
        self.url = url
        self.width = size[0]
        self.height = size[1]
        self.steps = steps

    def TextGenerate(self, prompt: str, emotion: str = None, name="untitled",
                     negative_prompt='{{nsfw,worst_quality}},mutated hands and fingers,text,title,deformed, '
                                     'bad anatomy, disfigured, poorly drawn face, mutation, mutated, extra limb, '
                                     'ugly, poorly drawn hands, missing limb, floating limbs, disconnected limbs, '
                                     'malformed hands, out of focus, long neck, long body',
                     sampler_index='Euler a', seed=-1,
                     cfg_scale=8):
        if name is None:
            name = "untitled"
        if emotion != '':
            prompt = "{{" + emotion + "}}, " + prompt
        Data = {'prompt': "{{best_quality,ultra-detailed,masterpiece,8k wallpaper}}, " + prompt,
                'negative_prompt': negative_prompt,
                'sampler_index': sampler_index,
                'seed': seed,
                'steps': self.steps,
                'width': self.width,
                'height': self.height,
                'cfg_scale': cfg_scale}
        print("prompt:" + "{{best_quality,ultra-detailed,masterpiece,8k wallpaper}}, " + prompt)
        print("negative_prompt:" + negative_prompt)
        Response = _submit_post(self.url + 'txt2img', Data)
        image = Response.json()['images'][0]
        return image, json.loads(Response.json()['info'])['seed']

    def ImageGenerate(self, prompt: str, emotion: str = None, name="untitled",
                      negative_prompt='{{nsfw,worst_quality}},mutated hands and fingers,text,title,deformed, '
                                      'bad anatomy, disfigured, poorly drawn face, mutation, mutated, extra limb, '
                                      'ugly, poorly drawn hands, missing limb, floating limbs, disconnected limbs, '
                                      'malformed hands, out of focus, long neck, long body',
                      sampler_index='Euler a', seed=-1,
                      cfg_scale=8,image: str = None):
        if name is None:
            name = "untitled"
        if emotion != '':
            prompt = "{{" + emotion + "}}, " + prompt
        Data = {'prompt': "{{best_quality,ultra-detailed,masterpiece,8k wallpaper}}, " + prompt,
                'negative_prompt': negative_prompt,
                'sampler_index': sampler_index,
                'seed': seed,
                'steps': self.steps,
                'width': self.width,
                'height': self.height,
                'cfg_scale': cfg_scale,
                'init_images': [image]}
        Response = _submit_post(self.url + 'img2img', Data)
        image = Response.json()['images'][0]
        return image, json.loads(Response.json()['info'])['seed']