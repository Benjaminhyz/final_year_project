from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

GOOGLE_API_KEY = 'AIzaSyAg3jErF2EDOZnPoIHan27VAOr8KG3cI2o'

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Restaurant Finder API. Use the /get-restaurants endpoint with a POST request."})

@app.route('/get-restaurants', methods=['POST'])
def get_restaurants():
    try:
        user_input = request.json
        query = user_input.get("query")
        location = user_input.get("location")
        radius = user_input.get("radius", 5000)

        if not query or not location:
            return jsonify({"success": False, "message": "Query and location are required"}), 400

        google_places_url = 'https://maps.googleapis.com/maps/api/place/textsearch/json'
        response = requests.get(google_places_url, params={
            "query": query,
            "location": location,
            "radius": radius,
            "key": GOOGLE_API_KEY
        })

        data = response.json()

        if response.status_code != 200 or "results" not in data:
            return jsonify({"success": False, "message": "Failed to fetch data from Google Maps API"}), 500

        results = []
        for place in data.get("results", []):
            results.append({
                "name": place.get("name"),
                "address": place.get("formatted_address"),
                "rating": place.get("rating", "N/A"),
                "opening_hours": place.get("opening_hours", {}).get("weekday_text", "No data available"),
                "google_maps_link": f"https://www.google.com/maps/place/?q=place_id:{place.get('place_id')}"
            })

        return jsonify({"success": True, "data": results})

    except Exception as e:
        app.logger.error(f"Error: {e}")
        return jsonify({"success": False, "message": "An error occurred while processing the request"}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
