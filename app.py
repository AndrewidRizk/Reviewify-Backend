from flask import Flask, jsonify, request, render_template, Response
from flask_cors import CORS
from places import main_get_total_reviews
from cohere_api import classify_reviews, summarize_reviews

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
messages = []
message = "🛜 listening on port /flask/process_data"
messages.append(message)
message = "✅ Back end Active"
messages.append(message)
import time
n = 0

def generate_messages():
    global messages
    global n
    while n != 1000:
        if messages:
            yield f"{messages.pop()}\n\n"
        else:
            # Add a short delay to avoid busy looping
            time.sleep(1)
            # Check for messages again after the delay
            if not messages:
                yield ""
        n = n + 1



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/stream')
def stream():
    return Response(generate_messages(), content_type='text/event-stream')


@app.route('/flask/process_data', methods=['POST'])
def process_data():
    global messages
    global n

    message = "🔌 Attempting to Connect to the Backend"
    messages.append(message)
    n = 0

    data = request.json  # Access JSON data sent from the form
    # Perform further processing if needed
    # Example: Extracting specific fields from the data
    restaurant = data.get('restaurant', '')  # getting the restaurant name
    postal = data.get('postal', '')  # getting the restaurant postal code
    if restaurant and postal:
        message = f"📬 Receiving Restaurant name: {restaurant} and Postal code: {postal}"
        messages.append(message)
        n = 0


    reviews_from_places = main_get_total_reviews(restaurant_name=restaurant, postal_code=postal)  # getting all the reviews
    message = "💻 Retrieving all Review "
    messages.append(message)
    n = 0


    # Calling the cohere functions
    # returning the classified results inputting the reviews and getting positive, negative, and unrelated
    classified_result, pos, neg, unrel = classify_reviews(reviews_from_places)
    # summarize the code
    message = "📝 Summarizing the Reviews"
    messages.append(message)
    n = 0


    try:
        summary = summarize_reviews(classified_result)
    except Exception  as e :
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
    n = 0

    return jsonify(response_data)