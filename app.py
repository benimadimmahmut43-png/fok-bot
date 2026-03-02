from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# ÖNEMLİ: API anahtarını buraya güvenli bir şekilde koy
API_KEY = "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"
URL = "https://api.groq.com/openai/v1/chat/completions"


@app.route('/')
def home():
    # Bu fonksiyon index.html dosyasını ekrana getirir
    return render_template('index.html')


@app.route('/get_response', methods=['POST'])
def get_response():
    user_text = request.json.get("message")

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": "Adın Fok. Samimi bir yapay zekasın. Türkçe konuş."},
            {"role": "user", "content": user_text}
        ]
    }
    headers = {"Authorization": f"Bearer {API_KEY}"}

    try:
        response = requests.post(URL, headers=headers, json=payload)
        bot_reply = response.json()["choices"][0]["message"]["content"]
        return jsonify({"reply": bot_reply})
    except:
        return jsonify({"reply": "Hata oluştu, API anahtarını kontrol et!"})


if __name__ == '__main__':
    app.run(debug=True)