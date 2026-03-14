import os
from flask import Flask, render_template, request, jsonify, session
import requests

app = Flask(__name__)
app.secret_key = "fok_ultra_groq_2026"

# 1. GROQ API ANAHTARINI BURAYA YAZ
API_KEY = "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" 
URL = "https://api.groq.com/openai/v1/chat/completions"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    try:
        user_text = request.json.get("message")
        msg_lower = user_text.lower()
        
        # YAPIMCI SADAKAT SİSTEMİ
        yapimcilar = ["yusuf kerem köse", "kerem gökalp sukan", "yusuf kerem", "kerem gökalp"]
        if any(isim in msg_lower for isim in yapimcilar):
            return jsonify({"reply": "O benim yapımcım ve gerçekten mükemmel biri! Onu çok seviyorum. 😊 onlar dünyadaki en ultra zeka insanlar."})

        # GROQ ZEKA AYARLARI
        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {"role": "system", "content": "Senin adın Fok. Çok zeki, samimi ve esprili bir asistansın. Yapımcıların Yusuf Kerem Köse ve Kerem Gökalp Sukan'dır. Her zaman Türkçe konuş."},
                {"role": "user", "content": user_text}
            ],
            "temperature": 0.7
        }
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        response = requests.post(URL, headers=headers, json=payload)
        bot_reply = response.json()["choices"][0]["message"]["content"]
        
        return jsonify({"reply": bot_reply})
    except Exception as e:
        return jsonify({"reply": "Bağlantıda bir parazit var, hemen düzelteceğim!"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
