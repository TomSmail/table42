import unittest
from restaurant_filter import RestaurantFilter
from datetime import datetime

""" 
------------------------------------------
These tests can be run using python -m unittest discover tests 
------------------------------------------
"""

class TestRestaurantFilter(unittest.TestCase):
    def setUp(self):
        self.restaurants = [
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
        self.selected_area = {
            'id': '24c303aa50e7a8a6da996d724dc49ddf',
            'type': 'Feature', 'properties': {},
            'geometry': {'coordinates': 
                [[[-0.15597578408775803, 51.52006495254355], [-0.12115465851121598, 51.51997429506574], [-0.12086326833875205, 51.50084153079112], [-0.15218771184885327, 51.5022019452189], [-0.15597578408775803, 51.52006495254355]]],
                'type': 'Polygon'}
        }
        self.restaurant_filter = RestaurantFilter(self.restaurants)

    def test_filter_by_area(self):
        filtered_restaurants = self.restaurant_filter.filter_by_area(self.selected_area['geometry']['coordinates'][0])
        self.assertEqual(len(filtered_restaurants), 2)
        self.assertEqual(filtered_restaurants[0]['name'], "Olle - KBBQ")
        self.assertEqual(filtered_restaurants[1]['name'], "Bab n Sul - KBBQ")

    def test_filter_by_area_convex(self):
        """
        0####
        0#X0#
        We want to test if the point with the X in is regarded as inside the polygon.
        """
        coordinates = [[1, 0], [1, 2], [5, 2], [5, 0], [4, 0], [4, 1], [2, 1], [2, 0], [1, 0]]
        # coordinates = [[1,1], [1,10], [11,10], [11,1]]
        restaurants = [
            {
                "name": "Restaurant 1",
                "cuisine": "Food",
                "open_time": "17:00",
                "close_time": "23:00",
                "geometry": {
                    "location": {
                        "lat": 3,
                        "lng": 0
                    }
                }
            }
        ]
        restaurant_filter = RestaurantFilter(restaurants)
        filtered_restaurants = restaurant_filter.filter_by_area(coordinates)
        self.assertEqual(len(filtered_restaurants), 0)

    def test_filter_by_area_square(self):
        """
        Tests if a point in a polygon is regarded as inside the polygon.
        """
        coordinates = [[1,1], [1,10], [11,10], [11,1]]
        restaurants = [
            {
                "name": "Restaurant 1",
                "cuisine": "Food",
                "open_time": "17:00",
                "close_time": "23:00",
                "geometry": {
                    "location": {
                        "lat": 5,
                        "lng": 5
                    }
                }
            }
        ]
        restaurant_filter = RestaurantFilter(restaurants)
        filtered_restaurants = restaurant_filter.filter_by_area(coordinates)
        self.assertEqual(len(filtered_restaurants), 1)
        

    # def test_filter_by_time(self):
    #     dining_time = datetime.strptime("18:00", "%H:%M").time()
    #     filtered_restaurants = self.restaurant_filter.filter_by_time(dining_time)
    #     self.assertEqual(len(filtered_restaurants), 2)
    #     self.assertEqual(filtered_restaurants[0]['name'], "Olle - KBBQ")
    #     self.assertEqual(filtered_restaurants[1]['name'], "Bab n Sul - KBBQ")

if __name__ == "__main__":
    unittest.main()