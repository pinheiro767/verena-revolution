import os
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# Pega a chave das variaveis de ambiente do Render
API_KEY = os.environ.get("GEMINI_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction="Voce e a Verena 2.0, assistente de IA Nativa Multimodal. Sua base e cientifica (PubMed) e juridica."
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        # Garante que estamos pegando o JSON corretamente
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({"response": "Dados invalidos."}), 400
            
        user_message = data.get("message")
        
        # Chama a IA do Google
        response = model.generate_content(user_message)
        
        if response and response.text:
            return jsonify({"response": response.text})
        else:
            return jsonify({"response": "A IA nao gerou uma resposta."}), 500
            
    except Exception as e:
        print(f"Erro no servidor: {e}")
        return jsonify({"response": f"Erro de conexao com a IA."}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)