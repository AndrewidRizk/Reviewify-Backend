from flask import Flask, jsonify, request, render_template, Response
from flask_cors import CORS
from places import main_get_total_reviews
from cohere_api import classify_reviews, summarize_reviews

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
messages = []  # Global variable to store messages
message = "🛜 listening on port /flask/process_data"
messages.append(message)
message = "✅ Back end Active"
messages.append(message)

@app.route('/')
def index():
    return render_template('index.html')  # Pass messages to the template


@app.route('/flask/process_data', methods=['POST'])
def process_data():
    data = request.json  # Access JSON data sent from the form
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


@app.route('/stream')
def stream():
    def generate():
        for message in messages:
            yield f"{messages.pop()}\n\n"
    return Response(generate(), content_type='text/event-stream')


