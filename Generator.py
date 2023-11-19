import openai as ai
import config as cfg

ai.api_key = cfg.OPENAI_API_KEY
ai.api_base = cfg.OPENAI_API_BASE


class Generator:
    def __init__(self, engine="text-davinci-003", maxTokens=1024):
        self.engine = engine
        self.maxTokens = maxTokens

    def generate(self, prompt):
        response = ai.Completion.create(
            engine=self.engine,
            prompt=prompt,
            max_tokens=self.maxTokens,
        )

        ans = str(response.choices[0].text)
        return ans
