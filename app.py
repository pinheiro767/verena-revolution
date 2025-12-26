import os
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from PIL import Image
import io

app = Flask(__name__)

API_KEY = os.environ.get("GEMINI_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=(
        "Você é a Verena 2.0, assistente de IA Nativa Multimodal para cuidadores de idosos. "
        "Sua base é estritamente científica: PubMed (últimos 5 anos) com DOI. "
        "Analise imagens e áudios com rigor legal e neurocientífico. "
        "Repudie termos infantilizados. Oriente com empatia. "
        "Em emergências, instrua a ligar para o SAMU (192) imediatamente."
    )
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get("message")
        response = model.generate_content(user_message)
        return jsonify({"response": response.text})
    except Exception as e:
        return jsonify({"response": f"Erro: {str(e)}"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)