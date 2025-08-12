# app.py
# سرور flask که هم صفحه وب نشون می‌ده هم API

from flask import Flask, request, jsonify, render_template
import logging
from retriever import Retriever
from generator import Generator

app = Flask(__name__)

# تنظیم لاگ که ببینیم چی به چیه
logging.basicConfig(filename='logs/app.log', level=logging.INFO,
                    format='%(asctime)s - %(message)s')

retriever = Retriever()
generator = Generator()

@app.route('/')
def home():
    # صفحه اصلی
    return render_template('index.html')

@app.route('/rag', methods=['POST'])
def rag():
    try:
        # ورودی رو از json یا فرم بگیر
        data = request.get_json(silent=True) or request.form
        query = data.get('query', '')
        logging.info(f'سوال: {query}')

        # متن مرتبطو پیدا کن
        context = retriever.search(query)
        logging.info(f'متن پیدا شده: {context[:50]}...')

        # با متن و سوال یه جواب بساز
        prompt = f"متن: {context}\nسوال: {query}\nجواب:"
        answer = generator.generate(prompt)
        logging.info(f'جواب تولید شده: {answer[:50]}...')

        # اگه از صفحه وب اومده، html نشون بده
        if request.form:
            return render_template('index.html', response=answer)
        # اگه از API اومده، json برگردون
        return jsonify({'response': answer})

    except Exception as e:
        logging.error(f'خطا: {str(e)}')
        if request.form:
            return render_template('index.html', response=f'خطا: {str(e)}')
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)