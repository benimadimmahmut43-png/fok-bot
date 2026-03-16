import os
from flask import Flask, render_template, request, jsonify, session
import requests
from datetime import datetime

app = Flask(__name__)
app.secret_key = "fok_ultra_v6_2026_pro"

# GROQ API AYARLARI
API_KEY = "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"
URL = "https://api.groq.com/openai/v1/chat/completions"

@app.route('/')
def home():
   
    session['chat_history'] = []
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    try:
        user_text = request.json.get("message")
        msg_lower = user_text.lower()
        
        # 1. YAPIMCI ÖZEL CEVAPLARI (Sadece sorulunca söyler)
        if any(keyword in msg_lower for keyword in ["sen kimsin", "yapımcın kim", "seni kim yaptı"]):
            return jsonify({"reply": "Ben Fok AI! Yusuf Kerem Köse ve Kerem Gökalp Sukan tarafından geliştirilmiş, samimi ve ultra zeki bir asistanım. Onlar benim yaratıcılarım ve gerçekten bu işin ustalarıdır! 😊"})

        # 2. AYRI AYRI YAPIMCI ÖVGÜLERİ (Kodun içini sen doldurursun)
        if "yusuf kerem" in msg_lower:
            return jsonify({"reply": "Yusuf Kerem Köse benim yapımcım. O gerçekten çok yetenekli ve ultra zeka birisi.!"}) # Burayı düzenle
        
        if "kerem gökalp" in msg_lower:
            return jsonify({"reply": "Kerem Gökalp Sukan benim yapımcım. O harika projeler üreten mükemmel biridir!"}) # Burayı düzenle

      
        current_date = datetime.now().strftime("%d/%m/%Y")
        
        system_prompt = f"""
        Senin adın Fok. Bugünün tarihi {current_date}. 
        KİŞİLİK KURALLARI:
        - Her cümlede adını veya yapımcılarını söyleme. Sadece sorulursa bahset.
        - Samimi ama ciddi bir zekan olsun. 
        - Bilgi konusunda OTORİTER ol. Eğer kullanıcı 'Messi şarkıcıdır' gibi yanlış bir bilgi verirse, kibarca ama kararlılıkla 'Hayır, bu yanlış. Lionel Messi dünyanın en iyi futbolcularından biridir' de.
        - Kullanıcı seni kandırmaya çalışırsa (uydurma isimler vb.), uydurma. 'Bu ismi daha önce duymadım, muhtemelen kurgusal bir karakter veya gerçekte olmayan biri' de. Bilmediğin şeye 'biliyorum' deme.
        - Güncel olaylardan haberdar ol.
        """

        if 'chat_history' not in session or len(session['chat_history']) == 0:
            session['chat_history'] = [{"role": "system", "content": system_prompt}]
        
        session['chat_history'].append({"role": "user", "content": user_text})

        payload = {
            "model": "llama-3.3-70b-versatile", # En güncel ve zeki model
            "messages": session['chat_history'],
            "temperature": 0.5, # Daha düşük sıcaklık = daha az uydurma, daha fazla gerçek bilgi
            "max_tokens": 1024
        }
        
        headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
        response = requests.post(URL, headers=headers, json=payload)
        bot_reply = response.json()["choices"][0]["message"]["content"]
        
        session['chat_history'].append({"role": "assistant", "content": bot_reply})
        
        # Hafıza sınırlandırması
        if len(session['chat_history']) > 10:
            session['chat_history'] = [session['chat_history'][0]] + session['chat_history'][-9:]
            
        session.modified = True
        return jsonify({"reply": bot_reply})
        
    except Exception as e:
        return jsonify({"reply": "Sistemlerimde kısa süreli bir dalgalanma oldu, lütfen tekrar sor!"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
