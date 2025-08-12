# retriever.py
# این کد متنای تو پوشه data رو می‌خونه و با مدل sentence-transformers پیداشون می‌کنه

from sentence_transformers import SentenceTransformer, util
import os

class Retriever:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')  # مدل سبک و خوب
        self.data_dir = 'data'
        self.texts = []
        self.embeddings = []
        self.load_texts()

    def load_texts(self):
        # هر فایل .txt تو data رو می‌خونیم
        for file in os.listdir(self.data_dir):
            if file.endswith('.txt'):
                with open(os.path.join(self.data_dir, file), 'r', encoding='utf-8') as f:
                    text = f.read().strip()
                    self.texts.append(text)
                    self.embeddings.append(self.model.encode(text))

    def search(self, query):
        # سوالو به embedding تبدیل می‌کنه و نزدیک‌ترین متنو پیدا می‌کنه
        query_emb = self.model.encode(query)
        similarities = util.cos_sim(query_emb, self.embeddings)[0]
        best_idx = similarities.argmax()
        return self.texts[best_idx]

retriever = Retriever()