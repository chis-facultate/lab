import paho.mqtt.client as mqtt
from pymongo import MongoClient
import time

BROKER = 'localhost'
TOPIC1 = 'senzor_1/temperatura'
TOPIC2 = 'senzor_2/temperatura'

# Configurare MongoDB
MONGO_URI = "mongodb+srv://user1:asdfsdfdzc13reqfvdf@cluster0.cve6w.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
mongo_client = MongoClient(MONGO_URI)
db = mongo_client['temperature_data_db']
collection = db['temperature_data_collection']


# Callback pentru procesarea mesajelor
def on_message(client, userdata, msg):
    topic = msg.topic
    temperature = float(msg.payload.decode())
    data = {
        "topic": topic,
        "temperature": temperature,
        "timestamp": time.time()
    }
    collection.insert_one(data)
    print(f"Saved to DB: {data}")


# Configurare client MQTT
def start_gateway():
    client = mqtt.Client()
    client.on_message = on_message
    client.connect(BROKER, 1883, 60)

    # Subscribe la topicurile senzorilor
    client.subscribe(TOPIC1)
    client.subscribe(TOPIC2)
    print("Gateway listening on topics:", TOPIC1, TOPIC2)

    client.loop_forever()


if __name__ == '__main__':
    start_gateway()
