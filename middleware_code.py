from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "Welcome to the Restaurant Finder API!"

@app.route("/get-restaurants", methods=["POST"])
def get_restaurants():
    try:
        # Extract data from the request
        data = request.json
        query = data.get("query")
        location = data.get("location")
        radius = data.get("radius", 5000)

        if not query or not location:
            return jsonify({"success": False, "message": "Query and location are required"}), 400

        # Mock response for testing purposes
        response = {
            "success": True,
            "data": [
                {"name": "Mock Restaurant 1", "address": "123 Main St.", "rating": 4.5},
                {"name": "Mock Restaurant 2", "address": "456 Elm St.", "rating": 4.0},
            ]
        }
        return jsonify(response)

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
