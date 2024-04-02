from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from places import main_get_total_reviews
from cohere_api import classify_reviews, summarize_reviews

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/flask/process_data', methods=['POST'])
def process_data():
    data = request.json  # Access JSON data sent from the form

    # Print the data to the console
    print("Data from Form:", data)



    # Perform further processing if needed
    # Example: Extracting specific fields from the data
    restaurant = data.get('restaurant', '')  # getting the restaurant name
    postal = data.get('postal', '')  # getting the restaurant postal code
    reviews_from_places = main_get_total_reviews(restaurant_name=restaurant, postal_code=postal)  # getting all the reviews

    # Calling the cohere functions
    # returning the classified results inputting the reviews and getting positive, negative, and unrelated
    classified_result, pos, neg, unrel = classify_reviews(reviews_from_places)
    # summarize the code
    summary = summarize_reviews(classified_result)

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
    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True)
