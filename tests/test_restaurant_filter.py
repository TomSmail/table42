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

    # def test_filter_by_time(self):
    #     dining_time = datetime.strptime("18:00", "%H:%M").time()
    #     filtered_restaurants = self.restaurant_filter.filter_by_time(dining_time)
    #     self.assertEqual(len(filtered_restaurants), 2)
    #     self.assertEqual(filtered_restaurants[0]['name'], "Olle - KBBQ")
    #     self.assertEqual(filtered_restaurants[1]['name'], "Bab n Sul - KBBQ")

if __name__ == "__main__":
    unittest.main()