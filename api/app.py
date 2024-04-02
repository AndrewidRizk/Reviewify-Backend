from flask import Flask, jsonify, request
from flask_cors import CORS
from places import main_get_total_reviews
from cohere_api import classify_reviews, summarize_reviews
app = Flask(__name__)
CORS(app) # Enable CORS for all routes

@app.route('/flask/process_data', methods=['POST'])
def process_data():
    data = request.json  # Access JSON data sent from React

    # Print the data to the console
    print("Data from React:", data)

    # You can also log it to a file if needed
    with open("data.log", "a") as f:
        f.write(str(data) + "\n")

    # Perform further processing if needed
    # Example: Extracting specific fields from the data
    restaurant = data.get('restaurant', '') # getting the restaurant name
    postal = data.get('postal', '') #getting the restaurant postal code
    reviews_from_places = main_get_total_reviews(restaurant_name=restaurant, postal_code=postal) # getting all the reviews
    
    # Calling the cohere functions
    # returning the classified results inputing the reviews and getting positive, negatiev, and unrelated
    classified_result, pos, neg, unrel = classify_reviews(reviews_from_places) 
    # samarize the code
    summary = summarize_reviews(classified_result)

    # Return a response
    
    positive = (pos/5)*100
    negative = (neg/5)*100
    unrelated = (unrel/5)*100

    # Construct response data
    response_data = {
        "resultStatus": "Success",
        'message': [positive, negative, unrelated, summary[0], summary[1]]
    }
    
    # Return processed data
    return jsonify(response_data)

    

