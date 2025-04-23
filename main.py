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
Estás gestionando campañas de Google Ads. Analiza este término:
Término: "{term}"
Campaña: "{campaign}"

Responde en JSON:
- irrelevant (true/false)
- reason (explicación breve)
- partial_term (palabra irrelevante, si aplica)
"""

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    try:
        result = eval(response.choices[0].message.content)
    except:
        result = {"irrelevant": False, "reason": "Respuesta no interpretable", "partial_term": ""}

    return jsonify(result)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
