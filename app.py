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

def generate_messages():
    global messages
    last_sent_index = 0
    while True:
        if last_sent_index < len(messages):
            yield f"{messages[last_sent_index]}\n\n"
            last_sent_index += 1
        else:
            yield ""

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/stream')
def stream():
    return Response(generate_messages(), content_type='text/event-stream')

@app.route('/flask/process_data', methods=['POST'])
def process_data():
    global messages
    message = "🔌 Attempting to Connect to the Backend"
    messages.append(message)
    data = request.json  # Access JSON data sent from the form
    restaurant = data.get('restaurant', '')  # getting the restaurant name
    postal = data.get('postal', '')  # getting the restaurant postal code
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
    return jsonify(response_data)