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
            self._load_page(url)
            available_times = self._extract_available_times()
            if available_times:
                notFound = False
            else:
                depth += 1
        wait = self._load_page(url)
        self._click_button_by_label('Book Now')
        available_times = self._extract_available_times()
        self._close()
        return available_times