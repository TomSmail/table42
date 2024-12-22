from weasyprint import HTML, CSS
import tempfile
import os 
import base64
import json
from mistralai import Mistral
from dotenv import load_dotenv
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
        # Load the environment variables
        load_dotenv()
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

    def _encode_image_to_base64(self, image_path):
        """
        Encodes a local image to base64 format.
        
        :param image_path: The path to the local image file.
        :return: The base64-encoded image string.
        """
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        return encoded_string
    
    def _get_button_to_next_page(self):
        """
        Gets the next page of the website.
        Updates the state of the drive to the next page.

        :return: If the times were found, return the times. Otherwise, return None.
        """

        api_key = os.environ["MISTRAL_API_KEY"]
        model = "pixtral-12b-2409"
        client = Mistral(api_key=api_key)

        # Get the image from the website
        image_path = self._get_website_image()
        encoded_image = self._encode_image_to_base64(image_path)

        # Define the messages for the chat
        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": 'Analyze the following image and provide the available reservation times or the next button to click to reach the reservation page. The output should be in the format: { "available_times": [time1, time2], "next_button": null } or { "available_times": null, "next_button": <button_text> }. If there are no available times and no next button, return { "available_times": null, "next_button": null }. Do NOT include any other information in the output.'
                    },
                    {
                        "type": "image_url",
                        "image_url": f"data:image/jpeg;base64,{encoded_image}" 
                    }
                ]
            }
        ]

        # Get the chat response
        chat_response = client.chat.complete(
            model=model,
            messages=messages
        )

        # Print the content of the response
        raw_result = chat_response.choices[0].message.content
        print(raw_result)
        # Try to covert the result to a dictionary
        try:
            result = json.loads(raw_result)
        except Exception as e:
            print(f"An error occurred while converting the result to a dictionary: {e}")
            return
        print(result)
        return result
        
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
    selenium_ai._get_button_to_next_page()
    selenium_ai._close()