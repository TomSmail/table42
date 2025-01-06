from weasyprint import HTML, CSS
import tempfile
import os 
import base64
import json
import time
import logging
import concurrent.futures
from datetime import datetime
from PIL import Image
from mistralai import Mistral
from dotenv import load_dotenv
from selenium import webdriver
from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from prompt_storage import PromptStorage

# Configure logging
logging.basicConfig(filename='all.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TimeRange:
    def __init__(self, start: datetime, end: datetime):
        """
        Initializes the TimeRange object with start and end times.
        
        :param start: The start time as a datetime.time object.
        :param end: The end time as a datetime.time object.
        """
        self.start = start
        self.end = end
    
    def get_end(self):
        return self.end.strftime("%A, %B %d, %Y %H:%M")
    
    def get_start(self):
        return self.start.strftime("%A, %B %d, %Y %H:%M")


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
        self.incorrect_button_labels = []
    
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
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        logging.info(f"Page loaded: {url}")

    def _click_button_by_label(self, label):
        permutations = self._generate_xpath_permutations(label.lower().capitalize())
        for perm in permutations:
            try:
                button = self.driver.find_element(By.XPATH, perm)
                if button.is_displayed() and button.is_enabled():
                    button.click()
                    logging.info(f"Button '{perm}' clicked successfully.")
                    return True
                else:
                    # Check if the parent node is interactable and click it
                    logging.info(f"Button '{perm}' is not interactable. Checking parent node.")
                    parent = button.find_element(By.XPATH, "..")
                    if parent.is_displayed() and parent.is_enabled():
                        parent.click()
                        logging.info(f"Parent of button '{perm}' clicked successfully.")
                        return True
            except NoSuchElementException:
                continue
        logging.info(f"No button with label permutations of '{label}' found, adding it to the list of incorrect buttons.")
        self.incorrect_button_labels.append(label)
        return False

    def _generate_label_permutations(self, label):
        """
        Generates permutations of the given label.
        
        :param label: The label to generate permutations for.
        :return: A list of permutations.
        """
        permutations = [label, label.lower().capitalize(), label.lower(), label.upper()]
        return permutations

    def _generate_xpath_permutations(self, label):
        """
        Generates permutations of the given label.
        
        :param label: The label to generate permutations for.
        :return: A list of permutations.
        """
        permutations = [f"button[title='{label}']",
                        f"//button[contains(text(), '{label}')]",
                        f"//button[text()='{label}']",
                        f"//button[.//span[text()='{label}']]",
                        f"//a[text()='{label}']"
                        ]
        return permutations
    
    def _close(self):
        self.driver.quit()

    def _get_website_image(self, permanent=False, save_path='website.png', quality=10):
        """
        Gets a screenshot of the website and compresses it.
        :param permanent: If True, the image will be saved permanently.
        :param save_path: The path to save the image.
        :param quality: The quality of the compressed image. 1-100 (100 is best).
        :return: The path to the compressed image.
        """

        try:
            # Ensure the page is fully loaded by waiting for a specific element
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )

            # Maximize the browser window
            self.driver.maximize_window()
            
            # Scroll to the top of the page
            self.driver.execute_script("window.scrollTo(0, 0);")
            
            # Create a file and save as img
            if permanent:
                self.driver.save_screenshot(save_path)
                logging.info(f"Permanent Screenshot saved at: {save_path}")
            else:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_img:
                    self.driver.save_screenshot(temp_img.name)
                    logging.info(f"Temporary PNG created at: {temp_img.name}")
                    save_path = temp_img.name

            # Open the image using Pillow
            image = Image.open(save_path)
            
            # Compress the image
            compressed_path = save_path.replace(".png", "_compressed.jpg")
            image.save(compressed_path, "JPEG", quality=quality)
            logging.info(f"Compressed image saved at: {compressed_path}")
            return compressed_path
        except Exception as e:
            logging.warning(f"An error occurred while extracting png link: {e}")
            return None

    def _get_website_html(self, save_path='website.html'):
        try:
            # Ensure the page is fully loaded by waiting for a specific element
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )

            # Get the html of the page
            html = self.driver.page_source
            with open(save_path, "w") as file:
                file.write(html)
            logging.info(f"HTML saved at: {save_path}")
            return save_path
        except Exception as e:
            logging.warning(f"An error occurred while extracting html link: {e}")
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
    
    def _get_button_to_next_page_or_times(self, time_range: TimeRange = TimeRange(datetime(datetime.now().year, datetime.now().month, datetime.now().day, 1), datetime(datetime.now().year, datetime.now().month, datetime.now().day, 23))) -> dict:
        """
        Prerequisite: The website must be loaded.

        Gets the next page of the website.
        Updates the state of the drive to the next page.
        The default time range is from 1am to 11pm and is disgusting. 
        
        :return: If the times were found, return the times. Otherwise, return None.
        """

        api_key = os.environ["MISTRAL_API_KEY"]
        model = "pixtral-12b-2409"
        client = Mistral(api_key=api_key)

        # Get the image from the website
        image_path = self._get_website_image()
        encoded_image = self._encode_image_to_base64(image_path)

        logging.info("Currently these are the incorrect button labels: " + str(self.incorrect_button_labels))
        content = PromptStorage.get("image_1", 
                    time_range=time_range, 
                    encoded_image=encoded_image, 
                    incorrect_button_labels=self.incorrect_button_labels
                    )
        # Define the messages for the chat
        messages = [
            {
                "role": "user",
                "content": content
            }
        ]

        def get_chat_response():
            return client.chat.complete(model=model, messages=messages)

        try:
            # Use ThreadPoolExecutor to run the function with a timeout
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(get_chat_response)
                chat_response = future.result(timeout=10)  # Timeout after 10 seconds
        except concurrent.futures.TimeoutError:
            logging.warning("The chat response took too long and timed out.")
            return None
        except Exception as e:
            logging.warning(f"An error occurred while getting the chat response: {e}")
            return None

        raw_result = chat_response.choices[0].message.content
        # Try to covert the result to a dictionary
        try:
            result = json.loads(raw_result)
            logging.info(f"Model Response: {result}")
        except Exception as e:
            logging.warning(f"An error occurred while converting the result to a dictionary: {e}")
            return None
        return result
    
    def _get_times(self, time_range: TimeRange = TimeRange(datetime(datetime.now().year, datetime.now().month, datetime.now().day, 1), datetime(datetime.now().year, datetime.now().month, datetime.now().day, 23))) -> list:
        """
        Prerequisite: The website must be loaded.

        Finds the available times displayed on the webpage
        
        :return: If the times were found, return the times.
        """

        api_key = os.environ["MISTRAL_API_KEY"]
        model = "pixtral-12b-2409"
        client = Mistral(api_key=api_key)

        # Get the image from the website
        image_path = self._get_website_image()
        encoded_image = self._encode_image_to_base64(image_path)
        prompt = f'''
                    Look at this image of a website reservation page,
                    if I wanted to book this restaurant at between
                    {time_range.get_start()} and {time_range.get_end()},
                    then would I be able to given the information you 
                    are given from the image? If you are able to then 
                    return the possible times you could book. Eg, if it
                    showed there was a table at 19:00 and 19:30
                    then you should return ["19:00", "19:30"]. If its not
                    possible to book the table between these times, then
                    just return []. DO NOT return anything else in the 
                    output. Please return in a 24 hour format 
                '''
        # Define the messages for the chat
        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    },
                    {
                        "type": "image_url",
                        "image_url": f"data:image/jpeg;base64,{encoded_image}" 
                    }
                ]
            }
        ]

        logging.debug(prompt)

        # Get the chat response
        chat_response = client.chat.complete(
            model=model,
            messages=messages
        )

        # Print the content of the response
        raw_result = chat_response.choices[0].message.content
        logging.debug(raw_result)
        # Try to covert the result to a list
        try:
            result = json.loads(raw_result)
        except json.JSONDecodeError:
            logging.warning("An error occurred whilst converting string list to list")
            result = []
        return result

    def _get_wait(self, seconds):
        """
        Returns a WebDriverWait object with the given number of seconds.
        
        :param seconds: The number of seconds to wait.
        :return: The WebDriverWait object.
        """
        return WebDriverWait(self.driver, seconds)
    
    def _close_popups(self):
        """
        Closes any popups that appear on the webpage.
        """
        try:
             # Wait for the alert to be present
            WebDriverWait(self.driver, 1).until(EC.alert_is_present())
            
            # Switch to the alert and dismiss it
            alert = self.driver.switch_to.alert
            alert.dismiss()
            logging.info("Alert dismissed successfully.")
        except Exception as e:
            logging.warning(f"An error occurred while closing popups: {e}")
        
    def walk_website(self, url):
        """
        Walks the website and finds the available times.
        
        :param url: The URL of the website to walk.
        :return: The available times if found, otherwise None.
        """
        depth = 0
        notFound = True
        available_times = []
        # IMPORTANT: PAGE MUST BE LOADED 
        self._load_page(url)
        while (notFound and depth < 5):
            depth += 1
            self._close_popups()
            page_dict = self._get_button_to_next_page_or_times()
            # Check if an error has occurred
            if page_dict is None:
                logging.warning("No page dict found.")
                return []
            logging.debug(f"Page dict: {page_dict}")
            if page_dict.get("available_times"):
                available_times = page_dict["available_times"]
                notFound = False
            elif page_dict.get("next_button"):
                num_pages = len(self.driver.window_handles)
                self._click_button_by_label(page_dict["next_button"])
                if num_pages != len(self.driver.window_handles):
                    logging.info("New tab opened.")
                    # Switch to the newly opened tab
                    self.driver.switch_to.window(self.driver.window_handles[-1])
                    # Wipe the incorrect button labels
                    self.incorrect_button_labels = []
                else:
                    logging.info("No new tab opened.")
            else:
                logging.warning("No available times or next button found.")
                # Early stopping
                return []
        return available_times


if __name__ == "__main__":
    driver_path = '/opt/homebrew/bin/chromedriver'
    url = "https://www.opentable.com/r/eleven-madison-park-new-york"
    selenium_ai = WebsiteWalker(driver_path=driver_path, headless=False)
    page_dict = selenium_ai.walk_website(url)
    print(page_dict)
    selenium_ai._close()