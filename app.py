from flask import Flask, request, jsonify, render_template
import datetime

app = Flask(__name__)

# Test data
RESTAURANTS = [
    {"name": "Olle - KBBQ", "cuisine": "Korean", "open_time": "17:00", "close_time": "23:00"},
    {"name": "Bab n Sul - KBBQ", "cuisine": "Korean", "open_time": "16:00", "close_time": "22:00"},
    {"name": "Haidilao - Hot Pot", "cuisine": "Chinese", "open_time": "12:00", "close_time": "23:00"},
]

@app.route("/")
def index():
    # Serve the HTML file
    return render_template("index.html") 

@app.route("/filter-restaurants", methods=["POST"])
def filter_restaurants():
    """
    Receives map selection and dining time from the frontend, 
    filters restaurants, and returns the filtered list.
    """
    data = request.json
    dining_time = data.get("dining_time")
    selected_area = data.get("map_selection")  # This is the GeoJSON from the frontend.

    if not dining_time or not selected_area:
        return jsonify({"error": "Invalid input"}), 400

    # Parse dining time
    dining_time = datetime.datetime.strptime(dining_time, "%H:%M").time()

    # Filter restaurants based on time
    available_restaurants = []
    for restaurant in RESTAURANTS:
        open_time = datetime.datetime.strptime(restaurant["open_time"], "%H:%M").time()
        close_time = datetime.datetime.strptime(restaurant["close_time"], "%H:%M").time()
        if open_time <= dining_time <= close_time:
            available_restaurants.append(restaurant)

    # Placeholder: You can filter based on the `selected_area` GeoJSON here.
    # Example: Check if the restaurant is within the selected area (requires GIS library like Shapely).

    return jsonify({"restaurants": available_restaurants})

if __name__ == "__main__":
    app.run(debug=True)
