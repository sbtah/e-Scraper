import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import (
    NoSuchElementException,
    ElementNotVisibleException,
)
from urllib.parse import urljoin
from lxml.html import fromstring, HTMLParser, HtmlElement
from scraper.helpers.logging import logging
from scraper.helpers.helpers import (
    random_sleep_small,
)


class BaseScraper:
    """"""

    def __init__(self, *args, **kwargs):
        self._driver = None
        self.teardown = True

    def __str__(self):
        return "Base Scraper"

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.driver.quit()

    @property
    def user_agent(self):
        return "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"

    @property
    def driver(self):

        if self._driver is None:
            options = webdriver.ChromeOptions()
            options.add_argument("--width=1920")
            options.add_argument("--height=1080")
            options.add_argument(self.user_agent)
            options.add_argument("--no-sandbox")
            options.add_argument("--start-maximized")
            options.add_argument("--single-process")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--incognito")
            # self.options.add_argument('--proxy-server=176.9.220.108:8080')
            # self.options.add_argument("--headless")
            options.add_argument("--disable-blink-features")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_argument("--disable-infobars")
            options.add_experimental_option("useAutomationExtension", False)
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            self._driver = webdriver.Remote(
                command_executor="http://192.168.95.3:4444/wd/hub",
                options=options,
            )

        return self._driver

    def parse_python_response(self, response_object) -> HtmlElement:
        """
        Used in parsing python requests objects to HtmlElements.
        ::param response_object:: requests object.
        """

        try:
            hp = HTMLParser(encoding="utf-8")
            element = fromstring(
                html=response_object.text,
                base_url=response_object.request.url,
                parser=hp,
            )
            logging.info(f"Parsing page to HTML at: {response_object.request.url}")
            return element
        except Exception as e:
            logging.error(f"Error parsing page to HTML: {e}")
            return None

    def parse_driver_response(self) -> HtmlElement:
        """
        Used with selenium driver current page_source.
        Doesn't need HTMLelement as an input.
        Parses current page and produce a HTMLElement from it.
        """

        try:
            hp = HTMLParser(encoding="utf-8")
            element = fromstring(
                self.driver.page_source, base_url=self.driver.current_url, parser=hp
            )
            logging.info(f"Parsing page to HTML at: {self.driver.current_url}")
            return element
        except Exception as e:
            logging.error(f"Error parsing page to HTML: {e}")
            return None

    def is_request_safe(self, html_element):
        """
        Validate our request on external service.
        Returns our user-agent and ip.
        If those dont match what we have setup, request won't be executed.
        """
        pass

    def selenium_get(self, url) -> HtmlElement:
        """
        Requests specified url by:
        :param url: Requested URL.
        Returns HtmlElement.
        """
        try:
            self.driver.get(url)
            random_sleep_small()
            page_element = self.parse_driver_response()
            return page_element
        except Exception as e:
            logging.error(f"(selenium_get) Exception: {e}")
            return None

    def python_get(self, url) -> HtmlElement:
        """
        Requests specified url by:
        :param url: Requested URL.
        Returns HtmlElement.
        """

        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
        }

        try:
            response = requests.get(url, timeout=30, headers=headers)
            random_sleep_small()
            response.raise_for_status()
            page_element = self.parse_python_response(response)
            return page_element
        except requests.exceptions.Timeout:
            logging.error("Connection was timed out.")
            return None
        except requests.exceptions.ConnectionError:
            logging.error("Connection Error.")
            return None
        except requests.exceptions.HTTPError:
            logging.error("HTTPError was raised.")
            return None
        except Exception as e:
            logging.error(f"(python_get) Exception: {e}")

    def get(self, url, type="Selenium") -> HtmlElement:

        if type == "Selenium":
            response = self.selenium_get(url)
            return response
        elif type == "Python":
            response = self.python_get(url)
            return response

    def request_url(self, url) -> HtmlElement:
        """
        Requests url.
        Returns HtmlElement.
        """
        if self.use_selenium and self.use_python:
            logging.error("!! use_selenium and use_python both set to True?")
            return None
        if self.use_selenium:
            element = self.get(url=url, type="Selenium")
            return element
        elif self.use_python:
            element = self.get(url=url, type="Python")
            return element
        else:
            logging.error("!! use_selenium or use_python need to be set to True.")
            return None

    def refresh_current_session(self):
        """
        Delete all cookies and refresh browser while using Selenium Driver.
        """
        self.driver.delete_all_cookies()
        self.driver.refresh()
        logging.info("Browser refreshed, cookies deleted.")

    def if_xpath_in_element(self, html_element, xpath_to_search) -> bool:
        """
        Looks for single object within provided HTMLElement.
        Returns True is successful.
        """
        try:
            html_element.xpath(xpath_to_search)[0]
            return True
        except IndexError:
            logging.error(
                f"(if_xpath_in_element) Search for: ('{xpath_to_search}') returned an empty list."
            )
            return None
        except Exception as e:
            logging.error(f"(if_xpath_in_element), EXEPTION: {e}")
            return None

    def wait_for_xpath_in_element(self, xpath_to_search, time_to_wait) -> HtmlElement:
        """
        Used with selenium driver.
        Waits for element to load to DOM for given time.
        Checks if specified Xpath is in HTML.
        Returns HTML document with loaded element that we looked for.
        """
        time.sleep(time_to_wait)
        html_document = self.parse_driver_response()
        try:
            html_document.xpath(xpath_to_search)[0]
            return html_document
        except IndexError:
            logging.error(f"Wait for: ('{xpath_to_search}') returned an empty list.")
            return None
        except Exception as e:
            logging.error(f"(wait_for_xpath_in_element), EXEPTION: {e}")
            return None

    def return_selenium_element(self, xpath_to_search):
        """
        Finds element by specified Xpath.
        Return Selenium element to interact with.
        """
        try:
            element = self.driver.find_element(
                By.XPATH,
                xpath_to_search,
            )
            return element
        except ElementNotVisibleException as e:
            logging.error(f"Selenium element not visible: {e}")
            return None
        except Exception as e:
            logging.error(f"Selenium element not visible: {e}")
            return None

    def initialize_element(self, xpath_to_click, xpath_to_check):
        """
        Used with selenium driver.
        Loads a part of content that is initialized on button click.
        Checks if desired element is in HTML
        Returns HTMLElement on success that can be parsed if other methods.
        ::param xpath_to_click:: Xpath to element that we have to click to
                                load desired element (ie: modal?).
        ::param xpath_to_check:: Xpath to element that we want in the DOM.
        """
        try:
            element_start_button = self.driver.find_element(
                By.XPATH,
                xpath_to_click,
            )
            element_start_button.click()
            logging.info("Successfully clicked on element initializer button.")
            try:
                random_sleep_small()
                html_after_click = self.parse_driver_response()
                html_after_click.xpath(xpath_to_check)[0]
                return html_after_click
            except IndexError as e:
                logging.error(f"Element not found: {e}")
                return None
            except Exception as e:
                logging.error(f"(initialize_element) Some other nasty exception: {e}")
                return None
        except NoSuchElementException:
            logging.error(
                "Failed at finding starting element to click. Maybe element is already picked?"
            )
            return None

    def close_element(self, xpath_to_check, xpath_to_click):
        """
        Used with selenium driver.
        Finds loaded HTML in the DOM by Xpath.
        Clicks on Xpath defined button that will close loaded element.
        On success returns HtmlElement without previous element in the DOM.
        ::param xpath_to_check:: Xpath of element that we want to close.
        ::param xpath_to_click:: Xpath of element that we have to click to close element.
        """

        try:
            element_close_button = self.driver.find_element(
                By.XPATH,
                xpath_to_click,
            )
            element_close_button.click()
            random_sleep_small()
            logging.info("Successfully clicked on element close button.")
            html_after_click = self.parse_driver_response()
            try:
                html_after_click.xpath(xpath_to_check)[0]
                logging.error(f"Modal was found, so it wasn't closed...")
                return None
            except IndexError:
                logging.info(
                    f"Check for element closed. Element not found, so it was closed..."
                )
                return html_after_click
            except Exception as e:
                logging.error(f"(close_element) Some other nasty exception: {e}")
                return None
        except NoSuchElementException:
            html_after_click = self.parse_driver_response()
            logging.info("Element not in the DOM nothing to close.")
            return html_after_click

    def send_text_to_input(self, text, xpath_to_find):
        """
        Locate an imput field by Xpath and sends value to it.
        """
        # Locate input element and send text value to it.
        try:
            input_el = self.driver.find_element(
                By.XPATH,
                xpath_to_find,
            )
            input_el.clear()
            input_el.send_keys(text)
            # Send value of store_name to server.
            input_el.send_keys(Keys.ENTER)
            random_sleep_small()
            logging.info(f"Successfuly send text: {text} to input field.")
        except ElementNotVisibleException:
            logging.error("Input field not in the DOM.")
        except Exception as e:
            logging.error(f"(send_text_to_input) Some other exception: {e}")

    def find_all_elements(self, html_element, xpath_to_search):
        """
        Xpath have to lead to entire HTML tag not attributes
        Finds elements by Xpath on given HTMLElement.
        Returns lists of HtmlElements for further processing.
        """
        try:
            elements_list = html_element.xpath(xpath_to_search)
            if elements_list:
                logging.info(
                    f"(find_all_elements), returned: {len(elements_list)} elements."
                )
                return elements_list
            else:
                logging.error("(find_all_elements) Returned an empty list.")
                return None
        except Exception as e:
            logging.error(f"(find_all_elements) Some other exception: {e}")
            return None

    def extract_urls_with_names(self, html_element, xpath_to_search, name_xpath):
        """
        Used for traversing page's url structure.
        Find all main Urls and 'Names' in given HtmlElements.
        Returns generator of tuples, containing (url, name).
        ::param name_xpath:: Can be set to ./text() or some other argument in tag.
        """
        categories_list = self.find_all_elements(
            html_element=html_element,
            xpath_to_search=xpath_to_search,
        )
        if categories_list:
            logging.info(
                f"URLS/Names list created, returned {len(categories_list)} elements."
            )
            return (
                (
                    urljoin(self.main_url, x.xpath(".//@href")[0]),
                    x.xpath(name_xpath)[0],
                )
                for x in categories_list
            )
        else:
            logging.info(f"Failed loading URLS/Names list from HTML,")
            return None
