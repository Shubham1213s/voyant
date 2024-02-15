from flask import Flask, render_template, jsonify, request
import paho.mqtt.client as mqtt

app = Flask(__name__)

# MQTT settings
mqtt_broker = "test.mosquitto.org"
mqtt_port = 1883
mqtt_topic = "voyant/RMScontrol/data2"

# Store received messages
received_messages = []

# MQTT on_message callback
def on_message(client, userdata, message):
    payload = message.payload.decode('utf-8')
    received_messages.append(payload)

# MQTT setup
mqtt_client = mqtt.Client()
mqtt_client.on_message = on_message
mqtt_client.connect(mqtt_broker, mqtt_port, 60)
mqtt_client.subscribe(mqtt_topic)

# Start MQTT loop in a separate thread
mqtt_client.loop_start()

@app.route('/')
def index():
    return render_template('index_live.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    message = request.form.get('message')
    mqtt_client.publish(mqtt_topic, message)
    return jsonify(status='success', message=message)

if __name__ == '__main__':
    app.run(debug=True, port = 5053)
