import os
import io
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from PIL import Image

app = Flask(__name__)

API_KEY = os.environ.get("GEMINI_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)

model = genai.GenerativeModel(model_name="gemini-1.5-flash")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_message = request.form.get("message")
        image_file = request.files.get("image")
        
        content_list = []
        if user_message: content_list.append(user_message)
        if image_file:
            img = Image.open(io.BytesIO(image_file.read()))
            content_list.append(img)

        # Instrução de sistema para manter a personalidade da Verena
        prompt = ["Voce e a Verena 2.0. Analise com base na PubMed e Direito do Idoso:"] + content_list
        
        response = model.generate_content(prompt)
        return jsonify({"response": response.text})
    except Exception as e:
        return jsonify({"response": f"Erro multimodal: {str(e)}"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)