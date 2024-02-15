from flask import Flask, render_template
import pymongo
from pymongo import MongoClient
import json
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = Flask(__name__)

@app.route('/')
def index():
    # Connect to MongoDB
    client = MongoClient('mongodb://localhost:27017')
    db = client.DevicesDB
    collection_name = "voyant/868019064428288/data"
    collection = db[collection_name]

    # Fetch data from MongoDB
    data = list(collection.find({}, {'_id': 0, 'message': 1}).sort('timestamp'))

    # Separate data into lists for plotting
    timestamps = []
    temp1_values = []
    temp2_values = []
    temp3_values = []
    temp4_values = []

    # Extract data from the list of dictionaries
    for entry in data:
        try:
            # Parse the JSON string in the "message" field
            message_data = json.loads(entry['message'])

            # Extract values
            timestamps.append(message_data['TimeStamp'])
            temp1_values.append(message_data['Temp1'])
            temp2_values.append(message_data['Temp2'])
            temp3_values.append(message_data['Humidity'])
            temp4_values.append(message_data['Pressure'])
        except (KeyError, json.JSONDecodeError) as e:
            print(f"Error extracting data: {e}")

    # Create the plot
    plt.figure(figsize=(10, 6))
    plt.plot(timestamps, temp1_values, label='Temp1', marker='o')
    plt.plot(timestamps, temp2_values, label='Temp2', marker='o')
    plt.plot(timestamps, temp3_values, label='Humidity', marker='o')
    plt.plot(timestamps, temp4_values, label='Pressure', marker='o')

    #plt.xticks(rotation='vertical')
    plt.xticks([])

    # Customize the chart
    plt.xlabel('Timestamp')
    plt.ylabel('Temperature, Humidity & Pressure')
    plt.title('Process Trends Over Time')
    plt.legend()
    plt.grid(True)

    # Convert the plot to a base64-encoded image
    image_stream = BytesIO()
    plt.savefig(image_stream, format='png')
    image_stream.seek(0)
    plot_image = base64.b64encode(image_stream.read()).decode('utf-8')

    # Render the HTML template with the plot
    return render_template('index_chart.html', plot_image=plot_image)

if __name__ == '__main__':
    app.run(debug=True, port = 5054)
