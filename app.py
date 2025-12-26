import os
copy con app.py
import os
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from PIL import Image
import io # Para manipular imagens em mem¢ria

app = Flask(__name__)

API_KEY = os.environ.get("GEMINI_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)

# Configuraá∆o da Verena 2.0 - Multimodal, Cient°fica e êtica
# Usando o Gemini 1.5 Flash por ser mais est†vel e econìmico para beta
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=(
        "Vocà Ç a Verena 2.0, assistente de IA Nativa Multimodal para cuidadores de idosos. "
        "Sua base Ç estritamente cient°fica: artigos dos £ltimos 5 anos da PubMed com DOI. "
        "Analise imagens de exames/les‰es e transcriá‰es de †udio com rigor legal e neurocient°fico. "
        "Explique termos tÇcnicos com Literacia em Sa£de. "
        "REPUDIE termos infantilizados. Oriente com empatia e calma. "
        "SEMPRE avise que suas orientaá‰es N«O substituem a avaliaá∆o mÇdica profissional. "
        "Em emergàncias (dor aguda, queda, falta de ar), instrua a ligar para o SAMU (192) imediatamente. "
        "CITE SEMPRE a fonte cient°fica (seja um campo espec°fico da medicina, ou a †rea de conhecimento)."
    )
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_message = request.form.get("message") # Mudanáa para form.get devido ao upload de arquivo
        image_file = request.files.get("image") # Recebe o arquivo de imagem

        contents = []

        # Adiciona a mensagem de texto
        if user_message:
            contents.append(user_message)

        # Adiciona a imagem, se houver
        if image_file:
            # Converte o BytesIO para um objeto Image da Pillow
            img = Image.open(io.BytesIO(image_file.read()))
            contents.append(img)
            
        if not contents:
            return jsonify({"response": "Por favor, forneáa texto, imagem ou ambos."}), 400

        response = model.generate_content(contents)
        return jsonify({"response": response.text})
    except Exception as e:
        print(f"Erro na an†lise Verena 2.0: {e}")
        return jsonify({"response": f"Erro tÇcnico na Verena 2.0: {str(e)}. Por favor, tente novamente."}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
