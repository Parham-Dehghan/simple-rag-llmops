# generator.py
# این کد با مدل distilgpt2 جواب تولید می‌کنه

from transformers import pipeline

class Generator:
    def __init__(self):
        self.gen = pipeline('text-generation', model='distilgpt2')  # مدل سبک

    def generate(self, prompt):
        # یه جواب کوتاه و معقول تولید می‌کنه
        result = self.gen(prompt, max_length=100, num_return_sequences=1)
        return result[0]['generated_text']

generator = Generator()