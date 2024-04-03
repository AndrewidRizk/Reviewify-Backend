from flask import Flask, jsonify, request, render_template, Response
from flask_cors import CORS
import time

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
messages = []
message = "🛜 Listening on port /flask/process_data"
messages.append(message)
message = "✅ Back end Active"
messages.append(message)

@app.route('/')
def index():
    return render_template('index.html', messages=messages)

@app.route('/stream')
def stream():
    def generate_messages():
        while True:
            if messages:
                yield f"{messages[-1]}\n\n"
                messages.clear()  # Clear the messages after sending
            else:
                time.sleep(1)  # Wait for 1 second before checking again

    return Response(generate_messages(), content_type='text/event-stream')

@app.route('/flask/process_data', methods=['POST'])
def process_data():
    data = request.json  # Access JSON data sent from the form
    restaurant = data.get('restaurant', '')  # getting the restaurant name
    postal = data.get('postal', '')  # getting the restaurant postal code
    if restaurant and postal:
        message = f"📬 Receiving Restaurant name: {restaurant} and Postal code: {postal}"
        messages.append(message)
        # Simulate processing time
        time.sleep(3)
        message = "💻 Retrieving all Reviews"
        messages.append(message)
        # Simulate processing time
        time.sleep(2)
        message = "📝 Summarizing the Reviews"
        messages.append(message)
        # Simulate processing time
        time.sleep(1)
        message = "📨 Sending the information back"
        messages.append(message)

    return jsonify({"status": "Processing data..."})

if __name__ == '__main__':
    app.run(debug=True)
