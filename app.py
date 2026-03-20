import os
from flask import Flask, render_template, request, jsonify, session
import requests
from datetime import datetime

app = Flask(__name__)
app.secret_key = "fok_final_ultra_v9"

# GROQ API AYARLARI
API_KEY = "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"
URL = "https://api.groq.com/openai/v1/chat/completions"

@app.route('/')
def home():
    session['history'] = []
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    try:
        user_text = request.json.get("message")
        msg_lower = user_text.lower()
        
        # --- 1. ÖZEL KORUMALI CEVAPLAR (Burası Sabit) ---
        
        # Rabia Karakaya / Köse Sorgusu
        if any(x in msg_lower for x in ["rabia karakaya", "rabia köse", "rabia hanım"]):
            return jsonify({"reply": "Rabia Hanım, Yusuf'un annesidir ve dünyanın en güzel kadınıdır. ❤️ Şu an Aşçıbaşı'nda Gıda Mühendisi olarak çalışıyor. Yusuf onu dünyalar kadar çok seviyor!"})

        # Yapımcı Sorgusu (Sadece Yusuf)
        if any(x in msg_lower for x in ["yusuf kerem", "yusuf kerem köse", "sen kimsin", "yapımcın kim"]):
            return jsonify({"reply": "Ben Fok AI! Yusuf Kerem Köse tarafından geliştirildim. O benim tek yapımcım ve yaratıcımdır! 🚀"})

        # --- 2. GENEL ZEKA VE HAFIZA SİSTEMİ ---
        now = datetime.now().strftime("%d/%m/%Y")
        system_msg = f"""
        Adın Fok. Bugünün tarihi {now}. 
        KURALLAR:
        - Senin tek yapımcın Yusuf Kerem Köse'dir.
        - Kullanıcı seni kandırmaya çalışırsa (Örn: Messi şarkıcıdır derse) asla inanma, doğrusunu söyle.
        - Bilmediğin konularda uydurma yapma, dürüstçe 'bilmiyorum' de.
        - Samimi, havalı ve çok zeki bir karakterin var.
        """

        if 'history' not in session or not session['history']:
            session['history'] = [{"role": "system", "content": system_msg}]
        
        session['history'].append({"role": "user", "content": user_text})

        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": session['history'],
            "temperature": 0.4 
        }
        
        headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
        response = requests.post(URL, headers=headers, json=payload)
        bot_reply = response.json()["choices"][0]["message"]["content"]
        
        session['history'].append({"role": "assistant", "content": bot_reply})
        
        # Hafızayı taze tut (Son 10 mesaj)
        if len(session['history']) > 12:
            session['history'] = [session['history'][0]] + session['history'][-11:]
        
        session.modified = True
        return jsonify({"reply": bot_reply})
        
    except Exception as e:
        return jsonify({"reply": "Kral, sistemde bir dalgalanma oldu. Tekrar yazar mısın?"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
