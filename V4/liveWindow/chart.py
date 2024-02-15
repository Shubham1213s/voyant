
import pymongo
from pymongo import MongoClient
import matplotlib.pyplot as plt
import json

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017')
db = client.DevicesDB
test2 = "voyant/868019064428288/data"
collection = db[test2]

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
        temp3_values.append(message_data['Temp3'])
        temp4_values.append(message_data['Temp4'])
    except (KeyError, json.JSONDecodeError) as e:
        print(f"Error extracting data: {e}")

# Plot the data
plt.figure(figsize=(10, 6))
plt.plot(timestamps, temp1_values, label='Temp1', marker='o')
plt.plot(timestamps, temp2_values, label='Temp2', marker='o')
plt.plot(timestamps, temp3_values, label='Temp3', marker='o')
plt.plot(timestamps, temp4_values, label='Temp4', marker='o')

# Customize the chart
plt.xlabel('TimeStamp')
plt.ylabel('Temperature')
plt.title('Temperature Trends Over Time')
plt.legend()
plt.grid(True)

# Show the chart
plt.show()
