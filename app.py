from flask import Flask, jsonify, request, render_template, Response
from flask_cors import CORS
from places import main_get_total_reviews
from cohere_api import classify_reviews, summarize_reviews
import threading
import time

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
messages = []
message = "🛜 Listening on port /flask/process_data"
messages.append(message)
message = "✅ Back end Active"
messages.append(message)

# Function to continuously check for new messages and push them to the client
def push_messages_to_client():
    global messages
    while True:
        time.sleep(1)  # Adjust sleep time as needed
        if len(messages) > 0:
            yield f"{messages.pop(0)}\n\n"  # Send the first message from the list to the client

# Start a separate thread to continuously push messages to the client
@app.route('/stream')
def stream():
    return Response(push_messages_to_client(), content_type='text/event-stream')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/flask/process_data', methods=['POST'])
def process_data():
    global messages
    message = "🔌 Attempting to Connect to the Backend"
    messages.append(message)
    data = request.json  # Access JSON data sent from the form
    # Perform further processing if needed
    # Example: Extracting specific fields from the data
    restaurant = data.get('restaurant', '')  # getting the restaurant name
    postal = data.get('postal', '')  # getting the restaurant postal code
    if restaurant and postal:
        message = f"📬 Receiving Restaurant name: {restaurant} and Postal code: {postal}"
        messages.append(message)

    reviews_from_places = main_get_total_reviews(restaurant_name=restaurant, postal_code=postal)  # getting all the reviews
    message = "💻 Retrieving all Review "
    messages.append(message)
    # Calling the cohere functions
    # returning the classified results inputting the reviews and getting positive, negative, and unrelated
    classified_result, pos, neg, unrel = classify_reviews(reviews_from_places)
    # summarize the code
    message = "📝 Summarizing the Reviews"
    messages.append(message)
    try:
        summary = summarize_reviews(classified_result)
    except Exception as e:
        message = f"❌ Error: {e}"
        messages.append(message)
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
    messages.append(message)
    return jsonify(response_data)

if __name__ == "__main__":
    threading.Thread(target=push_messages_to_client).start()  # Start the thread for pushing messages
    app.run(debug=True)
