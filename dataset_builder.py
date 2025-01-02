from google_list_scraper import GoogleMapsScraper
from google_restaurant_info import GoogleRestaurantInfo
from selenium_ai import WebsiteWalker
import os
import csv

class DatasetBuilder:
    def __init__(self, url="https://maps.app.goo.gl/bhNQ9nyFsgApCahHA"):
        self.google_restaurant_info = GoogleRestaurantInfo()
        self.google_maps_api = GoogleMapsScraper()
        self.url = url 
        self.walker = WebsiteWalker()

    def build_dataset(self):
        restaurant_names = self.google_maps_api.get_restaurant_names(self.url)
        websites = self.google_restaurant_info.get_websites_from_queries(restaurant_names)
        
        for website in websites:
            self.walker._load_page(website)
            base_url = os.path.dirname("dataset/")
            # Remove the protocol from the URL
            name = website.replace("http://", "").replace("https://", "").replace("www.", "")
            name = name.split(".")[0]
            screenshot_path = os.path.join(base_url, "screenshots", f"{name}.png")
            html_path = os.path.join(base_url, "html", f"{name}.html")
            self.walker._get_website_image(True, screenshot_path)
            self.walker._get_website_html(html_path)

            # write website url to csv
            with open("dataset/actions.csv", "a") as f:
                writer = csv.writer(f)
                writer.writerow([f"{website}", f"{screenshot_path}", f"{html_path}", " "])
            
            

if __name__ == "__main__":
    dataset_builder = DatasetBuilder()
    dataset_builder.build_dataset()
