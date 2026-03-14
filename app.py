import os
from flask import Flask, render_template, request, jsonify, session
import requests

app = Flask(__name__)
app.secret_key = "fok_ultra_v4_2026"

# GROQ API AYARLARI
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
        
        # --- YAPIMCI ÖZEL CEVAPLARI (BURAYI DÜZENLE) ---
        
        # Yusuf Kerem Köse için özel cevap
        if "yusuf kerem" in msg_lower:
            return jsonify({"reply": "O benim yaratıcılarımdan biri.o budala iyi çocuk ya. severiz.adımı ondan alıyorum. selam sana fokları biricik atası."})

        # Kerem Gökalp Sukan için özel cevap
        if "kerem gökalp" in msg_lower:
            return jsonify({"reply": "sohbeti de sarar, zaten geliştiricilerimden, ultra zeki, daha ne olsun. bi de penguen olmasaydı iyiydi enayi."})

        # ----------------------------------------------

        # Standart Zeka Yanıtı
        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {"role": "system", "content": "Senin adın Fok. Yapımcıların Yusuf Kerem Köse ve Kerem Gökalp Sukan'dır. Zeki, samimi ve havalısın."},
                {"role": "user", "content": user_text}
            ],
            "temperature": 0.7
        }
        headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

        response = requests.post(URL, headers=headers, json=payload)
        bot_reply = response.json()["choices"][0]["message"]["content"]
        
        return jsonify({"reply": bot_reply})
    except:
        return jsonify({"reply": "Bağlantıda küçük bir parazit var, hemen düzeliyorum!"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
