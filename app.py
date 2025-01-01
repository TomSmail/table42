from flask import Flask, request, jsonify, render_template
import datetime
import logging

from google_list_scraper import GoogleMapsScraper
from google_restaurant_info import GoogleRestaurantInfo
from restaurant_filter import RestaurantFilter

# Configure logging
logging.basicConfig(filename='all.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)

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
    selected_area = data.get("map_selection")  

    if not dining_time or not selected_area:
        return jsonify({"error": "Invalid input"}), 400

    # Parse dining time
    dining_time = datetime.datetime.strptime(dining_time, "%H:%M").time()

    # Grab the restaurant names from the Google Maps URL
    url = 'https://maps.app.goo.gl/SS8F4pbUHVw29FRv6'
    scraper = GoogleMapsScraper()
    restaurant_names = scraper.get_restaurant_names(url)
    google_maps_api = GoogleRestaurantInfo()
    restaurants = google_maps_api.get_details_from_queries(restaurant_names)

    # Filter restaurants based on time
    restaurant_filter = RestaurantFilter(restaurants)
    logging.info(f"Number of restaurants before filtering: {len(restaurants)}")
    # Filter restaurants by area
    filtered_restaurants = restaurant_filter.filter_by_area(selected_area['geometry']['coordinates'][0])
    logging.info(f"Number of restaurants after area filtering: {len(filtered_restaurants)}")
    # Filter restaurants by time
    filtered_restaurants = restaurant_filter.filter_by_time(dining_time)
    logging.info(f"Number of restaurants after area and time filtering: {len(filtered_restaurants)}")

    return jsonify({"restaurants": filtered_restaurants}), 200

if __name__ == "__main__":
    app.run(debug=True)
