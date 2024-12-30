import requests
from dotenv import load_dotenv
import os
from pprint import pprint

class GoogleRestaurantInfo:
    """
    This class is responsible for interacting with the Google Maps API to search for places,
    fetch place details, and extract websites.
    """

    def __init__(self):
        """
        Initializes the GoogleRestaurantInfo with the env API key.
        """
        load_dotenv()
        self.api_key = os.getenv("GOOGLE_MAPS_API_KEY")

    def search_place(self, query):
        """
        Searches for a place using the provided query and returns the place ID.
        
        :param query: The search query for the place.
        :return: The place ID if found, otherwise None.
        """
        url = f"https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={query}&inputtype=textquery&fields=place_id&key={self.api_key}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'OK' and data.get('candidates'):
                return data['candidates'][0]['place_id']
            else:
                print(f"Error searching for place: {data.get('status')}")
                return None
        else:
            print(f"Failed to retrieve the page. Status code: {response.status_code}")
            return None

    def _fetch_place_details(self, place_id):
        """
        Fetches the details of a place using the provided place ID.
        
        :param place_id: The place ID of the place to fetch details for.
        :return: The place details if found, otherwise None.
        """
        url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&key={self.api_key}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'OK':
                return data.get('result')
            else:
                print(f"Error fetching place details: {data.get('status')}")
                return None
        else:
            print(f"Failed to retrieve the page. Status code: {response.status_code}")
            return None

    def _fetch_websites_from_ids(self, place_ids):
        """
        Fetches the websites of places using the provided list of place IDs.
        
        :param place_ids: A list of place IDs.
        :return: A list of websites.
        """
        websites = []
        for place_id in place_ids:
            place_details = self._fetch_place_details(place_id)
            print(place_details)
            if place_details and 'website' in place_details:
                websites.append(place_details['website'])
        return websites

    def get_websites_from_queries(self, queries):
        """
        Searches for places using the provided queries and fetches their websites.
        
        :param queries: A list of search queries for the places.
        :return: A list of websites.
        """
        place_ids = []
        for query in queries:
            place_id = self.search_place(query)
            if place_id:
                place_ids.append(place_id)
        websites = self._fetch_websites_from_ids(place_ids)
        for website in websites:
            print(website)
        return websites
    
    def get_details_from_queries(self, queries):
        """
        Searches for places using the provided queries and fetches their details.
        
        :param queries: A list of search queries for the places.
        :return: A list of place details.
        """
        place_ids = []
        for query in queries:
            place_id = self.search_place(query)
            if place_id:
                place_ids.append(place_id)
        place_details = []
        for place_id in place_ids:
            details = self._fetch_place_details(place_id)
            if details:
                place_details.append(details)
        return place_details


if __name__ == "__main__":

    google_maps_api = GoogleRestaurantInfo()
    # Example queries for places
    queries = [
        'Los Mochis London City',
    ]
    result = google_maps_api.get_details_from_queries(queries)
    pprint(result)

    pprint(result[0]['geometry']['location'])