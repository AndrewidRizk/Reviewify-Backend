from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from places import main_get_total_reviews
from cohere_api import classify_reviews, summarize_reviews

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
socketio = SocketIO(app)  # Initialize Flask-SocketIO
messages = []
message = "🛜 Listening on port /flask/process_data"
messages.append(message)
message = "✅ Back end Active"
messages.append(message)

@app.route('/')
def index():
    return render_template('index.html', messages=messages)

@socketio.on('message')
def handle_message(message):
    messages.append(message)
    emit('update', message, broadcast=True)

@app.route('/flask/process_data', methods=['POST'])
def process_data():
    message = "🔌 Attempting to Connect to the Backend"
    socketio.emit('update', message, broadcast=True)
    data = request.json  # Access JSON data sent from the form
    # Perform further processing if needed
    # Example: Extracting specific fields from the data
    restaurant = data.get('restaurant', '')  # getting the restaurant name
    postal = data.get('postal', '')  # getting the restaurant postal code
    if restaurant and postal:
        message = f"📬 Receiving Restaurant name: {restaurant} and Postal code: {postal}"
        socketio.emit('update', message, broadcast=True)

    reviews_from_places = main_get_total_reviews(restaurant_name=restaurant, postal_code=postal)  # getting all the reviews
    message = "💻 Retrieving all Review "
    socketio.emit('update', message, broadcast=True)
    # Calling the cohere functions
    # returning the classified results inputting the reviews and getting positive, negative, and unrelated
    classified_result, pos, neg, unrel = classify_reviews(reviews_from_places)
    # summarize the code
    message = "📝 Summarizing the Reviews"
    socketio.emit('update', message, broadcast=True)
    try:
        summary = summarize_reviews(classified_result)
    except Exception as e:
        message = f"❌ Error: {e}"
        socketio.emit('update', message, broadcast=True)
    # Calculate percentages
    positive = (pos / 5) * 100
    negative = (neg / 5) * 100
    unrelated = (unrel / 5) * 100
    # Construct response data
    response_data = {
        "resultStatus": "Success",
        'message': [positive, negative, unrelated, summary[0], summary[1]]
    }
    # Return processed data
    message = "📨 Sending the information back"
    socketio.emit('update', message, broadcast=True)
    return jsonify(response_data)

if __name__ == '__main__':
    socketio.run(app, debug=True)
