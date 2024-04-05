from flask import Flask, jsonify, request, render_template, Response, session
from flask_cors import CORS
from places import main_get_total_reviews
from cohere_api import classify_reviews, summarize_reviews
import datetime

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
CORS(app)  # Enable CORS for all routes


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/flask/process_data', methods=['POST'])
def process_data():
    if 'messages' not in session:
        session['messages'] = []  # Initialize messages for the current session

    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    message = f"{current_time} | 🔌 - Attempting to Connect to the Backend"
    session['messages'].append(message)

    data = request.json  # Access JSON data sent from the form
    restaurant = data.get('restaurant', '')  # getting the restaurant name
    postal = data.get('postal', '')  # getting the restaurant postal code
    if restaurant and postal:
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        message = f"{current_time} | 📬 - Receiving Restaurant name: {restaurant} and Postal code: {postal}"
        session['messages'].append(message)

    reviews_from_places = main_get_total_reviews(restaurant_name=restaurant, postal_code=postal)
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    message = f"{current_time} | 💻 - Retrieving all Review "
    session['messages'].append(message)

    classified_result, pos, neg, unrel = classify_reviews(reviews_from_places)

    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    message = f"{current_time} | 📝 - Summarizing the Reviews"
    session['messages'].append(message)

    try:
        summary = summarize_reviews(classified_result)
    except Exception as e:
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        message = f"{current_time} | ❌ - Error: {e}"
        session['messages'].append(message)

    positive = (pos / 5) * 100
    negative = (neg / 5) * 100
    unrelated = (unrel / 5) * 100

    response_data = {
        "resultStatus": "Success",
        'message': [positive, negative, unrelated, summary[0], summary[1]]
    }

    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    message = f"{current_time} | 📨 - Sending the information back"
    session['messages'].append(message)

    return jsonify(response_data)


@app.route('/stream')
def stream():
    def generate():
        if 'messages' not in session:
            session['messages'] = []  # Initialize messages for the current session
        for message in session['messages']:
            yield f"{message}\n\n"

    return Response(generate(), content_type='text/event-stream')



