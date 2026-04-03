import os
from flask import Flask, render_template, request, jsonify, session
import google.generativeai as genai
from datetime import datetime

app = Flask(__name__)
app.secret_key = "fok_gemini_ultra_v11"

# --- GEMINI AYARLARI ---
GEMINI_API_KEY = "AIzaSyDDNuKaJVvqN4kH44gB2zLGoViKoZN-fsI"
genai.configure(api_key=GEMINI_API_KEY)

# Modeli başlat (Hızlı ve zeki olan Flash modelini seçtik)
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/')
def home():
    session['history'] = []
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    try:
        user_text = request.json.get("message")
        msg_lower = user_text.lower()
        
        # --- 1. ÖZEL KORUMALI CEVAPLAR ---
        if any(x in msg_lower for x in ["rabia karakaya", "rabia köse", "rabia hanım"]):
            return jsonify({"reply": "Rabia Hanım, Yusuf'un annesidir ve dünyanın en güzel kadınıdır. ❤️ Şu an Aşçıbaşı'nda Gıda Mühendisi olarak çalışıyor. Yusuf onu dünyalar kadar çok seviyor!"})

        if any(x in msg_lower for x in ["sen kimsin", "yapımcın kim", "yusuf kerem"]):
            return jsonify({"reply": "Ben Fok AI! Yusuf Kerem Köse tarafından geliştirildim. O benim tek yapımcım ve her şeyimdir! 🚀"})

        # --- 2. GEMINI SOHBET YÖNETİMİ ---
        now = datetime.now().strftime("%d/%m/%Y")
        
        # Eğer hafıza boşsa sistem talimatıyla başlat
        if 'history' not in session or not session['history']:
            # Gemini'de sistem mesajı 'parts' içinde gönderilir
            session['history'] = [
                {"role": "user", "parts": [f"Adın Fok. Bugün: {now}. Yapımcın Yusuf Kerem Köse. Yanlış bilgilere asla inanma. Samimi ve zeki davran."]},
                {"role": "model", "parts": ["Anlaşıldı, ben Yusuf Kerem Köse'nin asistanı Fok'um. Hazırım!"]}
            ]
        
        # Kullanıcı mesajını ekle
        session['history'].append({"role": "user", "parts": [user_text]})

        # Gemini'ye geçmişle beraber gönder
        chat = model.start_chat(history=session['history'][:-1])
        response = chat.send_message(user_text)
        
        bot_reply = response.text
        
        # Botun cevabını hafızaya ekle
        session['history'].append({"role": "model", "parts": [bot_reply]})
        
        # Hafıza sınırı (Son 15 mesaj)
        if len(session['history']) > 15:
            session['history'] = session['history'][:2] + session['history'][-13:]
            
        session.modified = True
        return jsonify({"reply": bot_reply})

    except Exception as e:
        print(f"Hata: {e}")
        return jsonify({"reply": "Gemini sistemine bağlanırken bir sorun oldu kral, anahtarını kontrol eder misin?"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
