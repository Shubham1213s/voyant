import flask
from flask import Flask, Blueprint, render_template,  request, jsonify
from pymongo import MongoClient
from flask_pymongo import PyMongo
import json
import paho.mqtt.client as mqtt

main_app = Flask(__name__)

main_app.config['MONGO_URI'] = 'mongodb://localhost:27017/MasterDB'
mongo = PyMongo(main_app)

client = MongoClient('mongodb://localhost:27017/')
db = client['MasterDB']  # Replace 'your_database_name' with your actual database name
collection = db['AllDevicesInfo']  # Replace 'your_collection_name' with your actual collection name

@main_app.route('/')
def index():
    data = list(collection.find())
    return render_template('index.html', data=data)

# Add a route to serve the CSS file
@main_app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)


@main_app.route('/templates/index_AddDevice')
def index_AddDevice():
    return render_template('index_AddDevice.html')

@main_app.route('/submit', methods=['POST'])
# def submit():
#     data = request.form.to_dict()
#     mongo.db.AllDevicesInfo.insert_one(data)
#     return jsonify({'message': 'Data added to MongoDB successfully'})
def submit():
    data = request.form.to_dict()
    imei_to_check = data.get('IMEI')
    # Check if a record with the given IMEI already exists
    existing_device = mongo.db.AllDevicesInfo.find_one({'IMEI': imei_to_check})
    if existing_device:
        # IMEI already exists, return an error
        return jsonify({'message': 'Device already exists with this IMEI'})
    else:
        # IMEI doesn't exist, insert data into MongoDB
        mongo.db.AllDevicesInfo.insert_one(data)
        return jsonify({'message': 'Data added to MongoDB successfully'})


@main_app.route('/templates/index_appShowAll')
def index_appShowAll():
    data = list(collection.find())
    return render_template('index_appShowAll.html', data=data)

@main_app.route('/templates/index')
def index_main():
    data = list(collection.find())
    return render_template('index.html', data=data)


# MongoDB settings
mongo_uri2 = 'mongodb://localhost:27017/'
mongo_db_name2 = 'DevicesDB'

@main_app.route('/templates/index_individual')
def index_individual():
    # Retrieve a list of all collections in the database
    client = MongoClient(mongo_uri2)
    db = client[mongo_db_name2]
    collections = db.list_collection_names()
    return render_template('index_individual.html', collections=collections)


# MQTT settings
mqtt_broker = "test.mosquitto.org"
mqtt_port = 1883
mqtt_topic = "voyant/868019064428288/data"
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


@main_app.route('/collection/<collection_name>')
def show_collection_data(collection_name):
    # Retrieve data from the specified collection
    client = MongoClient(mongo_uri2)
    db = client[mongo_db_name2]
    collection = db[collection_name]
    data = collection.find()
    return render_template('collection_data.html', collection_name=collection_name, data=data)

# Route to handle the /voyant/ route and its subpaths
@main_app.route('/collection/voyant/<path:subpath>')
def handle_voyant(subpath):
    collection_name = f'voyant/{subpath}'
    # Retrieve data from the specified collection
    client = MongoClient(mongo_uri2)
    db = client[mongo_db_name2]
    collection = db[collection_name]
    data = collection.find()
    return render_template('collection_data.html', collection_name=collection_name, data=data)


@main_app.route('/search', methods=['POST'])
def search():
    collection_name = request.form['searchInput']
    client = MongoClient(mongo_uri2)
    db = client[mongo_db_name2]
    # Check if the collection exists in the database
    if collection_name not in db.list_collection_names():
        return collection_name + ' is not existed.'
        #return render_template('error.html', message=f"Collection '{collection_name}' does not exist.")
    collection_data = db[collection_name].find()

    return render_template('result.html', collection_name=collection_name, collection_data=collection_data)


@main_app.route('/get_messages')
def get_messages():
    return jsonify(messages=received_messages)

if __name__ == '__main__':
    main_app.run(debug=True, port=5051)
