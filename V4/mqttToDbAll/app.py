import paho.mqtt.client as mqtt
from pymongo import MongoClient
from datetime import datetime
import json

# MQTT Broker settings
mqtt_broker = 'test.mosquitto.org'
mqtt_topic = 'voyant/#'             # Update the topic to subscribe to all subtopics under 'voyant'

# MongoDB settings
mongo_uri = 'mongodb://localhost:27017/'
mongo_db_name = 'DevicesDB'

# Connect to MongoDB
client = MongoClient(mongo_uri)
db = client[mongo_db_name]

# MQTT Callbacks
def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT Broker with result code {rc}")
    client.subscribe(mqtt_topic)

def on_message(client, userdata, msg):
    print(f"Received message on topic {msg.topic}: {msg.payload}")
    # Insert the received message into MongoDB
    collection = db[msg.topic]
    message_doc = {
        "topic": msg.topic,
        "message": msg.payload.decode('utf-8'),
    }
    collection.insert_one(message_doc)
    print("Inserted into MongoDB")

# Create MQTT client
mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

# Connect to MQTT Broker
mqtt_client.connect(mqtt_broker, 1883, 60)

# Start the MQTT loop
mqtt_client.loop_start()

# Keep the program running
try:
    while True:
        pass
except KeyboardInterrupt:
    print("Disconnected gracefully")
    mqtt_client.disconnect()
    client.close()
