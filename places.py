import requests
import pickle
import os

class Restaurant:
    def __init__(self, name, postal_code, location):
        self.name = name
        self.postal_code = postal_code
        self.location = location
        self.reviews = []

    def add_review(self, review):
        self.reviews.append(review)

    def __str__(self):
        return f"Name: {self.name}\nPostal Code: {self.postal_code}\nLocation: {self.location}"
    
API_KEY = os.getenv("api_key_Y2")  # Correct way

def get_reviews(restaurant):
    place_id = get_place_id(restaurant.name, restaurant.location)
    print(place_id)

    if place_id:
        reviews = get_reviews_text_by_place_id(place_id)
        return reviews
    else:
        return None

def get_place_id(restaurant_name, location):
    url = f'https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={restaurant_name} {location}&inputtype=textquery&key={API_KEY}'
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200 and 'candidates' in data and data['candidates']:
        return data['candidates'][0]['place_id']
    else:
        return None

def get_reviews_text_by_place_id(place_id):
    url = f'https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&key={API_KEY}'
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200 and 'result' in data and 'reviews' in data['result']:
        reviews_data = data['result']['reviews'][:10]
        review_texts = [review['text'] for review in reviews_data]
        return review_texts
    else:
        return None

  

def get_location_from_postal_code(postal_code, api_key):
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": postal_code,
        "region": "ca",
        "key": api_key,
    }

    try:
        response = requests.get(base_url, params=params)
        
        # Print the response status and content for debugging 
        
        if response.status_code != 200:
            return f"❌ API Error: {response.text}"

        data = response.json()  # This line might be failing if the response is empty
        
        if "results" in data and data["results"]:
            return data["results"][0].get("formatted_address", "Unknown Address")
        else:
            return f"⚠️ No location found for postal code: {postal_code}"

    except requests.exceptions.RequestException as e:
        return f"🚨 Request failed: {e}"


def main_get_total_reviews(restaurant_name, postal_code):
    #Input: Name of the restaurant and postal code
    #restaurant_name = 'Pita N More'
    #postal_code = 'L8S 1C5'

    # Get location from postal code
    location = get_location_from_postal_code(postal_code, API_KEY)

    # Create a Restaurant instance
    restaurant = Restaurant(restaurant_name, postal_code, location)

    # Get reviews from Places API
    reviews_from_places = get_reviews(restaurant)


    return reviews_from_places
