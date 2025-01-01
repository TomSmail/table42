import unittest
import requests

from selenium_ai import WebsiteWalker

class TestRestaurantFilter(unittest.TestCase):
    """
    PRE-REQUISITES: test_app.py must be running in a seperate terminal! 

    Run this test suite by executing the following command in the terminal:
    python -m unittest discover tests

    NOTE: The walker uses an external ai therefore it is non deterministic.

    """
    
    def test_index(self):
        r = requests.get('http://127.0.0.1:5000')
        self.assertEqual(r.status_code, 200)

    def test_button_getting(self):
        url = 'http://127.0.0.1:5000'
        walker = WebsiteWalker()

        walker._load_page(url)
        page_dict = walker._get_button_to_next_page_or_times()
        # Check if the page has a next button
        self.assertTrue(page_dict)
        self.assertTrue(page_dict['next_button'])

    def test_button_clicking(self):
        url = 'http://127.0.0.1:5000'
        walker = WebsiteWalker()

        walker._load_page(url)
        walker._click_button_by_label('Reservations')

        self.assertEqual(walker.driver.current_url,
                          'http://127.0.0.1:5000/reservations')
        
    def test_button_getting_and_clicking(self):
        pass 
        # TODO: Implement this test case

        

        
