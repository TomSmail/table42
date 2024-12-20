from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class GoogleMapsScraper:
    """
    This class is responsible for scraping the list of restaurants from a Google Maps URL.
    It uses Selenium to interact with the webpage and extract the restaurant names.
    The get_restaurant_names method takes a Google Maps URL as input and returns a list of restaurant names.
    """
    
    def __init__(self, driver_path='/opt/homebrew/bin/chromedriver', headless=True):
        self.driver_path = driver_path
        self.headless = headless
        self.driver = self._setup_driver()

    def _setup_driver(self):
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        service = Service(self.driver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        return driver

    def _load_page(self, url):
        self.driver.get(url)
        wait = WebDriverWait(self.driver, 20)
        return wait

    def _click_button_by_label(self, label):
        wait = WebDriverWait(self.driver, 20)
        try:
            button = wait.until(EC.presence_of_element_located((By.XPATH, f"//button[.//span[text()='{label}']]")))
            button.click()
            print(f"Button '{label}' clicked successfully.")
        except Exception as e:
            print(f"An error occurred while clicking the button '{label}': {e}")

    def _extract_restaurant_names(self):
        wait = WebDriverWait(self.driver, 20)
        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.fontHeadlineSmall')))
            restaurant_elements = self.driver.find_elements(By.CSS_SELECTOR, 'div.fontHeadlineSmall')
            restaurant_names = [element.text for element in restaurant_elements]
            return restaurant_names
        except Exception as e:
            print(f"An error occurred while extracting restaurant names: {e}")
            return []

    def _close(self):
        self.driver.quit()

    def get_restaurant_names(self, url):
        wait = self._load_page(url)
        self._click_button_by_label('Reject all')
        restaurant_names = self._extract_restaurant_names()
        self._close()
        return restaurant_names


if __name__ == "__main__":
    url = 'https://maps.app.goo.gl/SS8F4pbUHVw29FRv6'

    scraper = GoogleMapsScraper()
    restaurant_names = scraper.get_restaurant_names(url)
    for name in restaurant_names:
        print(name)