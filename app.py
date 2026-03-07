import os
from flask import Flask, render_template, request, jsonify, session
import requests

app = Flask(__name__)
# Hafızayı korumak için gerekli anahtar
app.secret_key = os.environ.get("SESSION_KEY", "fok_anahtar_v3_2026")

# 1. API ANAHTARIN (Burayı mutlaka kontrol et!)
# İstersen direkt tırnak içine yazabilirsin: API_KEY = "gsk_..."
API_KEY = "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" 
URL = "https://api.groq.com/openai/v1/chat/completions"

@app.route('/')
def home():
    # Sayfa açıldığında hafızayı temizle ve karakteri belirle
    session['history'] = [
        {"role": "system", "content": "Senin adın Fok. Çok zeki, yardımsever ve esprili bir asistansın. Her zaman Türkçe cevap ver."}
    ]
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    user_text = request.json.get("message")
    
    # Hafıza kontrolü
    if 'history' not in session:
        session['history'] = [{"role": "system", "content": "Adın Fok."}]
    
    history = session['history']
    history.append({"role": "user", "content": user_text})
    
    # Zeka Ayarları (Llama 3.3 70B)
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": history,
        "temperature": 0.7,
        "max_tokens": 1024
    }
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(URL, headers=headers, json=payload)
        # Eğer API'den hata gelirse terminale yazdır (Render Logs kısmında görürsün)
        if response.status_code != 200:
            print(f"API Hatası: {response.text}")
            return jsonify({"reply": "Şu an Groq servisine bağlanamıyorum, API anahtarını kontrol eder misin?"})
            
        bot_reply = response.json()["choices"][0]["message"]["content"]
        
        # Cevabı hafızaya ekle
        history.append({"role": "assistant", "content": bot_reply})
        session['history'] = history[-10:] # Son 10 mesajı hatırla
        session.modified = True
        
        return jsonify({"reply": bot_reply})
    except Exception as e:
        print(f"Sistem Hatası: {e}")
        return jsonify({"reply": "Bağlantımda bir parazit var, sanırım internetim kesildi!"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

