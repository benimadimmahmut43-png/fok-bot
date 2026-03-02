from flask import Flask, render_template, request, jsonify, session
import requests
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_KEY", "fok_super_zek_2024")

# Groq API Bilgileri
API_KEY = "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"
URL = "https://api.groq.com/openai/v1/chat/completions"

@app.route('/')
def home():
    # Sayfa açıldığında hafıza yoksa, botun kişiliğini tanımla
    if 'history' not in session:
        session['history'] = [
            {
                "role": "system", 
                "content": "Senin adın Fok. Dünyanın en gelişmiş ve güncel yapay zekalarından birisin. "
                           "Karakterin: Samimi, esprili ama çok profesyonel. "
                           "Kural 1: SADECE Türkçe konuş. "
                           "Kural 2: Bilmediğin konularda uydurma, dürüst ol. "
                           "Kural 3: Önceki mesajları asla unutma, kullanıcıyla gerçek bir bağ kur."
            }
        ]
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    user_text = request.json.get("message")
    if not user_text:
        return jsonify({"reply": "Dinliyorum, bir şey mi dedin?"})
    
    history = session.get('history', [])
    history.append({"role": "user", "content": user_text})
    
    # DAHA ZEKİ AYARLAR:
    payload = {
        "model": "llama-3.3-70b-versatile", # En gelişmiş Llama 3.3 modeli
        "messages": history,
        "temperature": 0.8, # Daha doğal ve akıcı cevaplar için
        "max_tokens": 2048, # Daha uzun ve detaylı cevaplar verebilir
        "top_p": 0.95,
        "stream": False
    }
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(URL, headers=headers, json=payload)
        response_data = response.json()
        bot_reply = response_data["choices"][0]["message"]["content"]
        
        # Hafızayı güncelle
        history.append({"role": "assistant", "content": bot_reply})
        
        # Hafıza sınırını 15 mesaja çıkardım (Daha fazla hatırlar)
        session['history'] = history[-15:]
        session.modified = True 
        
        return jsonify({"reply": bot_reply})
    except Exception as e:
        print(f"Hata: {e}")
        return jsonify({"reply": "Bağlantımda bir parazit var, tekrar söyler misin?"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
