from weasyprint import HTML, CSS
import tempfile
import os 
from mistralai import Mistral
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class WebsiteWalker:
    """
    This website walker class is for recursively stepping through a website
    and finding what times are available.
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

    def _close(self):
        self.driver.quit()

    def _get_website_image(self):
        try:
            # Create a temporary file and save as temp img
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_img:
                self.driver.save_screenshot(temp_img.name)
                print(f"Temporary PNG created at: {temp_img.name}")
                return temp_img.name
        except Exception as e:
            print(f"An error occurred while extracting png link: {e}")
            return None
    
    def _get_next_page(self):
        """
        Gets the next page of the website.
        Updates the state of the drive to the next page.

        :return: If the times were found, return the times. Otherwise, return None.
        """
        # TODO: Implement the logic to get the next page of the website.



        
    def walk_website(self, url):
        """
        Walks the website and finds the available times.
        
        :param url: The URL of the website to walk.
        :return: The available times if found, otherwise None.
        """
        depth = 0
        notFound = True
        available_times = []

        while (notFound and depth < 5):
            # TODO: Implement the website walking logic here.
            if available_times:
                notFound = False
            else:
                depth += 1
        
        return available_times

if __name__ == "__main__":
    driver_path = '/opt/homebrew/bin/chromedriver'
    url = 'https://www.losmochis.co.uk'

    selenium_ai = WebsiteWalker(driver_path=driver_path, headless=False)
    selenium_ai._load_page(url)
    temp_pdf_path = selenium_ai._get_website_image()
    selenium_ai._close()