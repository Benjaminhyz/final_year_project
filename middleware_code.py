from flask import Flask, request, jsonify
import os

# Initialize Flask app
app = Flask(__name__)

# Define the home route
@app.route("/")
def home():
    return "Welcome to the Restaurant Finder API!"

# Define the /get-restaurants POST endpoint
@app.route("/get-restaurants", methods=["POST"])
def get_restaurants():
    """
    Endpoint to simulate a restaurant search.
    Accepts JSON input with query, location, and radius parameters.
    """
    # Parse JSON data from the request
    data = request.json
    query = data.get("query")  # e.g., "halal food"
    location = data.get("location")  # e.g., "1.3039,103.8318"
    radius = data.get("radius", 5000)  # Default radius is 5000 meters

    # Mock response simulating restaurant results
    response = {
        "success": True,
        "data": [
            {
                "name": "Mock Restaurant",
                "address": "123 Example St.",
                "rating": 4.5
            },
            {
                "name": "Another Restaurant",
                "address": "456 Another St.",
                "rating": 4.0
            }
        ]
    }

    # Return the response as JSON
    return jsonify(response)

# Main entry point for running the Flask app
if __name__ == "__main__":
    # Get the PORT from the environment variable for Heroku
    port = int(os.environ.get("PORT", 5000))
    # Run the Flask app on all available network interfaces
    app.run(host="0.0.0.0", port=port)
