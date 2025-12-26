import os
import io
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from PIL import Image

app = Flask(__name__)

API_KEY = os.environ.get("GEMINI_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)

# AQUI ESTA A CORRECAO DO ERRO 404
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_message = request.form.get("message")
        image_file = request.files.get("image")
        
        content_list = []
        # AVISO LEGAL obrigatorio na instrução do sistema
        system_prompt = (
            "Voce e a Verena 2.0, uma IA de suporte a literacia em saude para cuidadores. "
            "IMPORTANTE: Voce NAO e medica. Suas respostas sao informativas e baseadas em protocolos cientificos (PubMed). "
            "Sempre oriente o usuario a consultar o médico responsavel pelo idoso e, em emergencias, ligar 192."
        )
        
        content_list.append(system_prompt)
        if user_message: content_list.append(user_message)
        if image_file:
            img = Image.open(io.BytesIO(image_file.read()))
            content_list.append(img)

        response = model.generate_content(content_list)
        return jsonify({"response": response.text})
    except Exception as e:
        return jsonify({"response": f"Erro tecnico: {str(e)}"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)