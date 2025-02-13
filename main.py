from places import main_get_total_reviews
from cohere_api import classify_reviews, summarize_reviews
import datetime
import time

def test_functionality():
    """Main function to test the functionality without running the Flask API."""
    
    # Sample input
    restaurant = "McDonalds"
    postal = "L8P4W3"

    # Logging the start time
    current_time = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]
    print(f"{current_time} | 🔍 - Starting test for: {restaurant}, Postal: {postal}")

    # Simulating the API processing steps
    try:
        reviews_from_places = main_get_total_reviews(restaurant_name=restaurant, postal_code=postal)
        print(f"{current_time} | ✅ - Retrieved {len(reviews_from_places)} reviews")
    except Exception as e:
        print(f"{current_time} | ❌ - Error retrieving reviews: {e}")
        return
    
    # Classifying reviews
    try:
        classified_result, pos, neg, unrel = classify_reviews(reviews_from_places)
        print(f"{current_time} | 📊 - Classified Reviews: Positive={pos}, Negative={neg}, Unrelated={unrel}")
    except Exception as e:
        print(f"{current_time} | ❌ - Error classifying reviews: {e}")
        return

    # Summarizing the reviews
    try:
        summary = summarize_reviews(classified_result)
        print(f"{current_time} | 📝 - Summary: {summary}")
    except Exception as e:
        print(f"{current_time} | ❌ - Error summarizing reviews: {e}")
        return
    
    # Calculate percentages
    positive_percentage = (pos / 5) * 100
    negative_percentage = (neg / 5) * 100
    unrelated_percentage = (unrel / 5) * 100

    # Display final output
    print("\n--- Final Output ---")
    print(f"Positive Reviews: {positive_percentage:.2f}%")
    print(f"Negative Reviews: {negative_percentage:.2f}%")
    print(f"Unrelated Reviews: {unrelated_percentage:.2f}%")
    print(f"Summary (Positive): {summary[0]}")
    print(f"Summary (Negative): {summary[1]}")

if __name__ == "__main__":
    test_functionality()
