import time
import random
import paho.mqtt.client as mqtt
import argparse


def publish_sensor_data(broker, port, topic, interval):
    client = mqtt.Client()
    client.connect(broker, port, 60)

    while True:
        temperature = round(random.uniform(20.0, 30.0), 2)  # Generează o temperatură aleatorie
        client.publish(topic, temperature)
        print(f"Sent: {temperature} to {topic}")
        time.sleep(interval)  # Trimite date la fiecare interval de secunde


if __name__ == '__main__':
    # Configurare argumente din linia de comandă
    parser = argparse.ArgumentParser(description="Simulate temperature sensor sending data via MQTT.")
    parser.add_argument('--topic', type=str, required=True, help="MQTT topic to publish data to.")

    args = parser.parse_args()

    # Configurare implicită pentru broker și alte valori
    BROKER = 'localhost'
    PORT = 1883
    INTERVAL = 5  # Intervalul între trimiteri (secunde)

    # Rulează funcția cu topic-ul specificat
    publish_sensor_data(BROKER, PORT, args.topic, INTERVAL)
