from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from places import main_get_total_reviews
from cohere_api import classify_reviews, summarize_reviews
from flask_socketio import SocketIO, emit
import redis

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app)

messages = []
message = "🛜 Listening on port /flask/process_data"
messages.append(message)
message = "✅ Back end Active"
messages.append(message)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/flask/process_data', methods=['POST'])
def process_data():
    global messages
    message = "🔌 Attempting to Connect to the Backend"
    messages.append(message)
    data = request.json
    restaurant = data.get('restaurant', '')
    postal = data.get('postal', '')
    if restaurant and postal:
        message = f"📬 Receiving Restaurant name: {restaurant} and Postal code: {postal}"
        messages.append(message)

    reviews_from_places = main_get_total_reviews(restaurant_name=restaurant, postal_code=postal)
    message = "💻 Retrieving all Review "
    messages.append(message)
    classified_result, pos, neg, unrel = classify_reviews(reviews_from_places)
    message = "📝 Summarizing the Reviews"
    messages.append(message)
    try:
        summary = summarize_reviews(classified_result)
    except Exception as e:
        message = f"❌ Error: {e}"
        messages.append(message)

    positive = (pos / 5) * 100
    negative = (neg / 5) * 100
    unrelated = (unrel / 5) * 100

    response_data = {
        "resultStatus": "Success",
        'message': [positive, negative, unrelated, summary[0], summary[1]]
    }

    message = "📨 Sending the information back"
    messages.append(message)

    # Emit event to notify clients about new message
    socketio.emit('new_message', {'message': response_data})

    return jsonify(response_data)

@app.route('/stream')
def stream():
    return jsonify(messages)