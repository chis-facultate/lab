import time
import requests
# URL-ul serverului FastAPI
url = "http://127.0.0.1:8000/sensor"
# Citirea fișierului și trimiterea datelor către server
with open("sensor_data.txt", "r") as file:
     for line in file:
 # Parsăm linia curentă
         timestamp, sensor_type, value = line.strip().split(", ")

         # Creăm payload-ul de trimis la server
         data = {
         "timestamp": int(timestamp),
         "sensor_type": sensor_type,
         "value": float(value)
         }
         # Trimitem cererea POST către server
         response = requests.post(url, json=data)

         # Verificăm dacă cererea a avut succes
         if response.status_code == 200:
             print(f"Data sent: {data}")
         else:
             print(f"Failed to send data: {data}")
         # Așteaptă 5 s
         time.sleep(5)