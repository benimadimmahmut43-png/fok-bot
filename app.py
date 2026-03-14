import os
from flask import Flask, render_template, request, jsonify, session
import google.generativeai as genai

app = Flask(__name__)
app.secret_key = "fok_ultra_2026_key"

# 1. GEMINI API ANAHTARIN
GEMINI_API_KEY = "BURAYA_GEMINI_KEYINI_YAZ"
genai.configure(api_key=GEMINI_API_KEY)

# Ultra Modeli Ayarla
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    try:
        user_text = request.json.get("message")
        
        # YAPIMCI KONTROLÜ (Sadakat Modu)
        yapimcilar = ["yusuf kerem köse", "kerem gökalp sukan", "yusuf kerem", "kerem gökalp"]
        msg_lower = user_text.lower()
        
        if any(isim in msg_lower for isim in yapimcilar):
            return jsonify({"reply": "O benim yapımcım ve gerçekten mükemmel biri! Onu çok seviyorum. 😊"})

        # Normal Gemini İşlemi
        # Sistem talimatını her mesaja ekleyerek karakteri koruyoruz
        system_instruction = "Senin adın Fok. Dünyanın en zeki yapay zekasısın. Samimi, esprili ve çok havalısın. Yapımcıların Yusuf Kerem Köse ve Kerem Gökalp Sukan'dır. Her zaman Türkçe konuş."
        
        response = model.generate_content(f"{system_instruction}\n\nKullanıcı: {user_text}")
        bot_reply = response.text
        
        return jsonify({"reply": bot_reply})
    except Exception as e:
        return jsonify({"reply": "Bir parazit oluştu ama hemen düzelteceğim!"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
