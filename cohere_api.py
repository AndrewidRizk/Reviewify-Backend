import cohere
from cohere import ClassifyExample
co = cohere.Client("fjykocFMg6C8cig1iRFmUokDM0dlKBYNA4KZKToy") #ADD KEY HERE

def classify_reviews(inputs):
  examples=[
    #Positive reviews
    ClassifyExample(text="I loved this restaurant. Nicest McDonald's location that I've been too. The store was very busy both at the drive thru and the inside. Plenty of seating inside, either downstairs or upstairs. I liked the view from the upstairs dining portion. The selection and freshness of the baked goods here was excellent. In the New York stores there isn't as much of baked good selections.", label="positive"), 
    ClassifyExample(text="Tried the new Chicken Big Mac. Really good. Maybe even better than the regular Big Mac. I got it hot off the grill, and they didn't skimp on the Special Sauce. Wish they would do a vegetarian option, though. Just replace the patties with old school veggie burgers (not those new lab-grown varieties).", label="positive"),
    ClassifyExample(text="The Mighty McMuffin!   Wow. My two favs up to now are the sausage McMuffin and the bacon McMuffin. More you can get them together. Had to get two.",label="positive"), 
    ClassifyExample(text="This is a great place. I visited when the restaurant was overwhelmed with orders with long quest of cu see Homer's to be served, but throughout, the staffs we calms friendly in attending and ensuring all customers were promptly served.", label="positive"), 
    ClassifyExample(text="I would recommend this to others", label="positive"),
    #Negative reviews
    ClassifyExample(text="Why do you accept skip orders when you are too busy to take them? 1.5 hours of waiting for your restaurant and can't even bloody confirm if you're making my food or not. Do you have no respect for customers? Reject the order when it comes in if you're so busy!", label="negative"), 
    ClassifyExample(text="manager was being beyond aggressive to one of the employees. yelling in front of the whole restaurant to “help”. when he did, she yelled at him again and then later yelled at him for not taking orders at the counter. don’t know where she thinks she works but it’s not that deep.", label="negative"), 
    ClassifyExample(text="worst mcdonalds location. Staff are beyond ridiculous after repeating myself for which drink i had wanted 4 times in a row they still gave me the wrong drink , asked for a tray to carry our food to dining area and was given a drink tray. Not to mention finding hair in our food and the dining area being absolutely filthy.", label="negative"),
    ClassifyExample(text="Not clean. Keeping the restaurant clean doesn't seem to be a priority. Washrooms are better to avoid. Order gets cleared from queue without completion for multiple customers, takes follow ups to get it and still not what was ordered. Eventually everything got fixed, but it took much longer than usual. A lot of staff seem to be lost and afraid to engage with customers. There are a few employees that seem to be pulling the workload for the rest of the team.", label= "negative"),
    ClassifyExample(text="Service was super slow whenever there were 7 employees or more behind the counter. Waited over 20 minutes for 2 happy meals and only one customer has been served since. Employees don't care, they are slow. 3 over 4 of the ordering screens were not working properly, and most of the customers use them; as employees were calling order numbers while the ordering screens did not provide any receipts. The place was filthy.", label="negative"),
    #Unrelated reviews
    ClassifyExample(text="The elephants in the kitchen were a unique touch. I've never had a salad tossed by a pachyderm before, but it added to the ambiance. Five stars for creativity!",label= "unrelated"),
    ClassifyExample(text="The menu was written in hieroglyphics, and I don't speak ancient Egyptian. Tried ordering the 'Pharaoh's Feast,' ended up with a pyramid of marshmallows. Confusing, but surprisingly tasty.", label="unrelated"),
    ClassifyExample(text="The chef must have mistaken my order for a treasure map because my dish arrived with an 'X' marked in chocolate syrup. Couldn't find any gold, but the dessert was golden.", label="unrelated"),
    ClassifyExample(text="I asked for a burger without pickles, but they served me a pickle sandwich without the bread. The staff insisted it was a 'deconstructed masterpiece.' I call it a cucumber catastrophe.",label= "unrelated"),
    ClassifyExample(text="The waitstaff was friendly, but the chairs were actually disguised robots. One of them tried to tell me a knock-knock joke. It's a restaurant, not a comedy club. Points for unexpected entertainment.",label= "unrelated"),
  ]

  #Categorize reviews using cohere classify method
  response = co.classify(
    inputs=inputs,
    examples=examples,
  )
  
  # Extract classifications from the response
  # Extract classifications from the response
  classifications = response.classifications

  # Initialize counts
  positive = 0
  negative = 0
  unrelated = 0

  # Initialize an empty list to store classified results
  classified_result = []

  # Iterate through each item in the classifications
  for item in classifications:
      # Assuming each item is a dictionary-like object
      prediction = item.prediction

      # Increment counts based on the prediction
      if prediction == 'positive':
          positive += 1
      elif prediction == 'negative':
          negative += 1
      elif prediction == 'unrelated':
          unrelated += 1

      # Append the text and label of the item to classified_result
      classified_result.append([item.input, prediction])

  return classified_result, positive, negative, unrelated

def summarize_reviews(classified_reviews):
  positive_text = "Summarize the following to 2-3 sentences in an informative fashion, in third person, and with a general tone (don't mention names), picking key words that peopple like (Quality, Quanity, service, etc). If no reviews provided after the ':' just say 'no reviews': "
  negative_text = "Summarize the following to 2-3 sentences in an informative fashion, in third person, and with a general tone (don't mention names), picking key words that peopple like (Quality, Quanity, service, etc). If no reviews provided after the ':' just say 'no reviews': "

  #Concatenate positive and negative reviews to their respective strings
  for i in classified_reviews:
    if (i[1] == 'positive'):
      if len(i[0]) > 420:
         positive_text += positive_text + " " + i[0][:420]
      else:
        positive_text += positive_text + " " + i[0]
    elif (i[1] == 'negative'):
      if len(i[0]) > 420:
         negative_text += negative_text + " " + i[0][:420]
      else:
        negative_text += negative_text + " " + i[0]

  #Summarize reviews and present it in an informative tone using coheres chat function
  positive_response = co.chat(
	  message=positive_text, 
	  model="command", 
	  temperature=0.9
  )

  negative_response = co.chat(
	  message=negative_text, 
	  model="command", 
	  temperature=0.9
  )

  #Split the test by the '\n' character, since the last line of the chat response is irrelevant information
  positive_summary = positive_response.text.split('\n', 1)
  negative_summary = negative_response.text.split('\n', 1)

  return [positive_summary[0], negative_summary[0]]