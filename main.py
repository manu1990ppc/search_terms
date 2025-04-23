from flask import Flask, request, jsonify
from openai import OpenAI
import os
import traceback
import sys

app = Flask(__name__)
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

@app.route('/analyze', methods=['POST'])
def analyze_term():
    try:
        data = request.json
        if data is None:
            return jsonify({"error": "No se pudo leer el cuerpo JSON"}), 400

        term = data.get('search_term')
        campaign = data.get('campaign_name')

        prompt = (
            f"Estás gestionando campañas de Google Ads. Analiza este término:\n"
            f"Término: \"{term}\"\n"
            f"Campaña: \"{campaign}\"\n\n"
            f"Responde en JSON:\n"
            f"- irrelevant (true/false)\n"
            f"- reason (explicación breve)\n"
            f"- partial_term (palabra irrelevante, si aplica)"
        )

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )

        raw_content = response.choices[0].message.content

        try:
            result = eval(raw_content)
        except Exception as parse_error:
            print("⚠️ Error al interpretar la respuesta de GPT:", file=sys.stderr)
            print("Contenido devuelto por GPT:\n", raw_content, file=sys.stderr)
            traceback.print_exc(file=sys.stderr)
            return jsonify({
                "error": "Respuesta no interpretable como JSON",
                "raw_content": raw_content,
                "exception": str(parse_error)
            }), 500

        return jsonify(result)

    except Exception as e:
        print("❌ Error interno en /analyze:", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
