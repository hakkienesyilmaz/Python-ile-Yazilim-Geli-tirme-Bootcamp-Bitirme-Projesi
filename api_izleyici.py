import requests
import time
import csv
from datetime import datetime

SLEEP_INTERVAL = 5 * 60
API_URL = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=try"
LOG_FILE = "log.csv"

def get_api_data(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status() 
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"API'ye bağlanılamadı veya istek başarısız oldu: {e}")
        return None

def write_to_csv(data):
    try:
        try_price = data['bitcoin']['try']
        birim = "BTC/TRY"
    except (TypeError, KeyError):
        print("API verisi beklenmedik formatta. API yanıtını kontrol et.")
        return
        
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    row = [timestamp, birim, try_price]

    file_exists = False
    try:
        with open(LOG_FILE, 'r') as f:
            if f.read(1): 
                file_exists = True 
    except FileNotFoundError:
        pass 

    try:
        with open(LOG_FILE, 'a', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile)

            if not file_exists:
                csv_writer.writerow(["Zaman Damgası", "Takip Birimi", "Fiyat (TRY)"])     
            csv_writer.writerow(row)
            print(f"[{timestamp}] Başarıyla loglandı: {birim} Fiyatı = {try_price:,.2f} TL")

    except Exception as e:
        print(f"Hata: CSV dosyasına yazma başarısız oldu: {e}")

def main_monitor():
    print(f"Bitcoin Fiyat İzleyici Başlatıldı")
    print(f"İzleme Aralığı: {SLEEP_INTERVAL // 60} dakika")
    print("-" * 39)

    while True:
        data = get_api_data(API_URL)
        if data:
            write_to_csv(data)       
        time.sleep(SLEEP_INTERVAL)

if __name__ == "__main__":
    try:
        main_monitor()
    except KeyboardInterrupt:
        print("\nİzleyici durduruldu (Kullanıcı tarafından).")
    except Exception as e:
        print(f"Beklenmedik bir hata oluştu: {e}")