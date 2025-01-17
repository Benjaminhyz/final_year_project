from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Replace this with your Google Maps API key
GOOGLE_API_KEY = 'AIzaSyAg3jErF2EDOZnPoIHan27VAOr8KG3cI2o'


@app.route('/get-restaurants', methods=['POST'])
def get_restaurants():
    """
    Endpoint to fetch restaurants based on user query and location.
    """
    try:
        # Extract user input from chatbot
        user_input = request.json
        query = user_input.get("query")  # e.g., 'halal food'
        location = user_input.get("location")  # e.g., '1.3039,103.8318' (Orchard Road)
        radius = user_input.get("radius", 5000)  # Search radius in meters (default is 5 km)

        if not query or not location:
            return jsonify({"success": False, "message": "Query and location are required"}), 400

        # Google Maps Places API endpoint
        google_places_url = 'https://maps.googleapis.com/maps/api/place/textsearch/json'

        # Make the API call to Google Maps
        response = requests.get(google_places_url, params={
            "query": query,
            "location": location,
            "radius": radius,
            "key": GOOGLE_API_KEY
        })

        data = response.json()

        if response.status_code != 200 or "results" not in data:
            return jsonify({"success": False, "message": "Failed to fetch data from Google Maps API"}), 500

        # Extract restaurant details
        results = []
        for place in data.get("results", []):
            results.append({
                "name": place.get("name"),
                "address": place.get("formatted_address"),
                "rating": place.get("rating", "N/A"),
                "opening_hours": place.get("opening_hours", {}).get("weekday_text", "No data available"),
                "google_maps_link": f"https://www.google.com/maps/place/?q=place_id:{place.get('place_id')}"
            })

        # Return results to chatbot
        return jsonify({"success": True, "data": results})

    except Exception as e:
        # Log the error for debugging
        app.logger.error(f"Error: {e}")
        return jsonify({"success": False, "message": "An error occurred while processing the request"}), 500


# Run the Flask server
if __name__ == '__main__':
    # Use Heroku's $PORT environment variable if available, otherwise default to 5000
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
