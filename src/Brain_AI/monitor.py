import requests
import time
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
def get_cpu_usage():
    # Prometheus API adresi
    url = "http://localhost:9090/api/v1/query"
    # CPU kullanımını hesaplayan PromQL sorgusu
    query = 'avg(irate(node_cpu_seconds_total{mode!="idle"}[2m])) * 100'
    
    try:
        response = requests.get(url, params={'query': query}, timeout=5)
        results = response.json()['data']['result']
        if results:
           
            return float(results[0]['value'][1])
        return 0.0
    except Exception as e:
        print(f"⚠️ Prometheus'tan veri çekilemedi: {e}")
        return 0.0


load_dotenv()

# Bilgiler koda gömülü değil, .env'den okunuyor.
SENDER_EMAIL = os.getenv("SENDER_EMAIL")       #SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD") #SENDER_PASSWORD=your_app_password
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")   # RECEIVER_EMAIL=receiver_email@gmail.com


last_mail_time = 0  # Son mailin gönderildiği zaman
MAIL_COOLDOWN = 300 # 5 dakika boyunca yeni mail atma
# --- E-POSTA ---
def send_ai_report(subject, body):
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        server.quit()
        print("✅ E-posta başarıyla gönderildi!")
    except Exception as e:
        print(f"❌ E-posta hatası: {e}")


def ask_ai_advisor(cpu_value):
    url = "http://127.0.0.1:11434/api/generate"
    data = {
        "model": "gemma2:2b",
        "prompt": f"""Analiz et: CPU %{cpu_value:.2f}. 
        Bir sistem mühendisi günlüğüne kısa bir teknik not düşüyormuşsun gibi cevap ver. 
        Asla tanım yapma, 'nedir' diye anlatma. 
        Eğer %80 altındaysa sadece 'Sistem stabil, yük dengeli.' gibi çok kısa bir cümle kur. 
        Eğer %80 üzeriyse doğrudan teknik müdahale önerisini yaz.""",
        "stream": False
    }
    try:
        response = requests.post(url, json=data, timeout=60)
        return response.json().get('response', 'Yanıt yok.')
    except:
        return "AI bağlantı hatası."

# --- ANA DÖNGÜ  ---
while True:
    
    cpu = get_cpu_usage() 
    print(f"\n[{time.strftime('%H:%M:%S')}] Mevcut CPU: %{cpu:.2f}")

    #  AI'ya analiz ettir
    print("🧠 AI Analiz Ediyor...")
    answer = ask_ai_advisor(cpu)
    print(f"🤖 Gemma: {answer}")

    # 3. MANTIKSAL BİRLEŞTİRME (ALARM TETİKLEYİCİ)
    if cpu > 80:
        current_time = time.time() # Şu anki zamanı saniye cinsinden al
        
        # Eğer (Şu anki zaman - Son mail zamanı) 5 dk dan büyükse mail at
        if current_time - last_mail_time > MAIL_COOLDOWN:
            print("🚨 Kritik seviye! E-posta gönderiliyor...")
            konu = f"Kritik Alarm: CPU %{cpu:.2f}"
            send_ai_report(konu, answer)
            
            # Mail gitti, şimdi kronometreyi sıfırla 
            last_mail_time = current_time 
        else:
            kalan_sure = int(MAIL_COOLDOWN - (current_time - last_mail_time))
            print(f"⏳ Alarm durumu devam ediyor ama bekleme süresindeyim. (Kalan: {kalan_sure} sn)")

    time.sleep(10)