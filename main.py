from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route('/analyze', methods=['POST'])
def analyze_term():
    data = request.json
    term = data.get('search_term')
    campaign = data.get('campaign_name')

    prompt = f"""
Estás ayudando a gestionar campañas publicitarias en Google Ads. 
Analiza el siguiente término de búsqueda dentro del contexto de una campaña llamada "{campaign}".

Término: "{term}"

Responde en formato JSON con:
- "irrelevant": true o false
- "reason": breve justificación
- "partial_term": si hay una parte irrelevante, indícalo (por ejemplo, "segunda mano")

Usa sentido común, patrones comunes irrelevantes (opiniones, tutoriales, etc.) y si el término no se alinea con productos típicos del nombre de la campaña.
"""

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    try:
        result = eval(response.choices[0].message.content)
    except:
        result = {
            "irrelevant": False,
            "reason": "No se pudo interpretar el análisis",
            "partial_term": ""
        }

    return jsonify(result)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
