import json
import base64
import requests
import config as cfg


def _save_encoded_image(b64_image: str, output_path: str):
    with open(output_path, 'wb') as image_file:
        image_file.write(base64.b64decode(b64_image))
    return b64_image


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
        if emotion is not None:
            prompt = "{{" + emotion + "}}, " + prompt
        print(prompt)
        Data = {'prompt': "{{best_quality,ultra-detailed,masterpiece,8k wallpaper}}, " + prompt,
                'negative_prompt': negative_prompt,
                'sampler_index': sampler_index,
                'seed': seed,
                'steps': self.steps,
                'width': self.width,
                'height': self.height,
                'cfg_scale': cfg_scale}
        Response = _submit_post(self.url, Data)
        image = _save_encoded_image(Response.json()['images'][0], 'txt2img/' + name + '.png')
        return image, json.loads(Response.json()['info'])['seed']