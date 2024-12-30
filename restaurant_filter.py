from pprint import pprint

class RestaurantFilter:
    def __init__(self, restaurants):
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
        pass
        # TODO: Implement this method
        # def criteria(restaurant):
        #     open_time = datetime.datetime.strptime(restaurant["open_time"], "%H:%M").time()
        #     close_time = datetime.datetime.strptime(restaurant["close_time"], "%H:%M").time()
        #     return open_time <= dining_time <= close_time
        
        # return self.filter(criteria)

if __name__ == "__main__":
    # Example data
    restaurants = [
        {
            "name": "Olle - KBBQ",
            "cuisine": "Korean",
            "open_time": "17:00",
            "close_time": "23:00",
            "geometry": {
                "location": {
                    "lat": 51.512069,
                    "lng": -0.131557
                }
            }
        },
        {
            "name": "Bab n Sul - KBBQ",
            "cuisine": "Korean",
            "open_time": "16:00",
            "close_time": "22:00",
            "geometry": {
                "location": {
                    "lat": 51.51187820780646,
                    "lng": -0.12389412811535294
                }
            }
        },
        {
            "name": "Haidilao - Hot Pot",
            "cuisine": "Chinese",
            "open_time": "12:00",
            "close_time": "23:00",
            "geometry": {
                "location": {
                    "lat": 51.50146071399152,
                    "lng": -0.12483826577778245
                }
            }
        },
        {
            "name": "Shitshack",
            "cuisine": "Caribean",
            "open_time": "12:00",
            "close_time": "23:00",
            "geometry": {
                "location": {
                    "lat": 51.60146071399152,
                    "lng": -0.16597578408775803
                }
            }
        }
    ]
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
    # filtered_restaurants = restaurant_filter.filter_by_time("18:00")
    # pprint(filtered_restaurants)