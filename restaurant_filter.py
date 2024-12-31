from pprint import pprint

from google_list_scraper import GoogleMapsScraper
from google_restaurant_info import GoogleRestaurantInfo
from selenium_ai import WebsiteWalker

class RestaurantFilter:
    def __init__(self, restaurants):
        """
        Restaurant list should be a list of dictionaries gathered from the 
        Google Places API.
        """
        self.restaurants = restaurants

    def filter(self, criteria):
        return [restaurant for restaurant in self.restaurants if criteria(restaurant)]
    
    def filter_by_area(self, coordinates):
        def criteria(restaurant):
            """
            Check if the restaurant is within the selected area
            We do this by making a line from the restaurant to some arbitrary 
            point outside the area and checking how many times it intersects 
            with the area. 
            """

            lat = restaurant['geometry']['location']['lat']
            lng = restaurant['geometry']['location']['lng']
            test_line = {'lat1': lat, 'lng1': lng, 'lat2': 0.0, 'lng2': 0.0}
            sides = []
            prev = coordinates[0]
            for i in range(len(coordinates)):
                if i == 0:
                    # Skip the first point as its prev
                    continue
                side = {'lat1': prev[1], 'lng1': prev[0], 'lat2': coordinates[i][1], 'lng2': coordinates[i][0]}
                prev = coordinates[i]
                sides.append(side)
            
            intersections = 0
            for side in sides:
                # Check if the test line intersects with the side
                if (test_line['lat1'] > side['lat1']) != (test_line['lat2'] > side['lat1']) and (test_line['lng1'] < side['lng1'] or test_line['lng2'] < side['lng1']):
                    intersections += 1
            
            return intersections % 2 == 1
            
        return self.filter(criteria)
    
    def filter_by_time(self, dining_time):
        """
        TODO: Check if dining time is in the same format as restaurant_times
        """
        def criteria(restaurant):
            walker = WebsiteWalker()
            google_maps_api = GoogleRestaurantInfo()
            info = google_maps_api.get_details_from_queries([restaurant['name']])
            
            if info[0].get('website'):
                print(f"Walking website of {restaurant['name']}")
                print(info[0]['website'])
                restaurant_times = walker.walk_website(info[0]['website'])
            else:
                # If the website is not available, we can't get the restaurant times
                print(f"Could not get the website for {restaurant['name']}")
                return False
            return dining_time in restaurant_times
            
        return self.filter(criteria)

if __name__ == "__main__":
    # Example data
    url = 'https://maps.app.goo.gl/SS8F4pbUHVw29FRv6'

    scraper = GoogleMapsScraper()
    restaurant_names = scraper.get_restaurant_names(url)
    google_maps_api = GoogleRestaurantInfo()
    restaurants = google_maps_api.get_details_from_queries(restaurant_names)
    
    selected_area = {
                    'id': '24c303aa50e7a8a6da996d724dc49ddf',
                    'type': 'Feature', 'properties': {},
                    'geometry': {'coordinates': 
                        [[[-0.15597578408775803, 51.52006495254355], [-0.12115465851121598, 51.51997429506574], [-0.12086326833875205, 51.50084153079112], [-0.15218771184885327, 51.5022019452189], [-0.15597578408775803, 51.52006495254355]]],
                        'type': 'Polygon'}
                    }

    # Create a RestaurantFilter object
    restaurant_filter = RestaurantFilter(restaurants)
    
    # Filter restaurants by area
    filtered_restaurants = restaurant_filter.filter_by_area(selected_area['geometry']['coordinates'][0])
    pprint(filtered_restaurants)
    # Filter restaurants by time
    filtered_restaurants = restaurant_filter.filter_by_time("18:00")
    pprint(filtered_restaurants)