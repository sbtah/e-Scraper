from datetime import datetime
from selenium.webdriver.support.ui import Select
from lxml.html import HTMLParser, document_fromstring, fromstring
from scraper.helpers.logger import logger
from scraper.helpers.randoms import (
    get_random_user_agent,
    random_sleep_small,
    random_sleep_small_l2,
)
from selenium.webdriver.remote.webelement import WebElement
from scraper.options.settings import USER_AGENTS
from selenium import webdriver
from selenium.common.exceptions import (
    ElementNotVisibleException,
    NoSuchElementException,
    ElementClickInterceptedException,
)
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager


class BaseScraper:
    """Base scraper class for other specialized scrapers."""

    def __init__(self, *args, **kwargs):
        self._driver = None
        self.teardown = True
        self.logger = logger
        self.time_started = datetime.now()

    def __str__(self):
        return "Base Scraper"

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.driver.delete_all_cookies()
            self.driver.quit()

    @property
    def user_agent(self):
        agent = get_random_user_agent(USER_AGENTS)
        return agent

    @property
    def potenial_popups_xpaths(self):
        """Should return a list of Xpaths to can appear on the Website randomly."""
        raise NotImplementedError

    @property
    def cookies_close_xpath(self):
        """Xpath to element that closes cookies policy banner on click."""
        raise NotImplementedError

    @property
    def driver(self):

        if self._driver is None:
            options = webdriver.ChromeOptions()
            options.add_argument("--width=1920")
            options.add_argument("--height=1080")
            # TODO:
            # Call get_random_user_agent to use different User-Agent server on each request..
            options.add_argument(f"user-agent=[{self.user_agent}]")
            options.add_argument("--no-sandbox")

            options.add_argument("--single-process")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--incognito")
            # TODO:
            # Call get_random_proxy to use different proxy server on each request..
            # self.options.add_argument('--proxy-server=176.9.220.108:8080')
            # options.add_argument("--headless")
            options.add_argument("--disable-blink-features")
            options.add_argument(
                "--disable-blink-features=AutomationControlled"
            )  # noqa
            options.add_argument("--disable-infobars")
            options.add_argument("--ignore-ssl-errors=yes")
            options.add_argument("--ignore-certificate-errors")
            # Deprecated ?
            # options.add_experimental_option("useAutomationExtension", False)
            options.add_experimental_option(
                "excludeSwitches",
                ["enable-automation"],
            )
            options.add_argument("--start-maximized")

            # Locally installed browser just for testing.
            # self._driver = webdriver.Chrome(
            #     service=Service(ChromeDriverManager().install()),
            #     options=options,
            #     desired_capabilities=DesiredCapabilities.CHROME,
            # )
            # self._driver.implicitly_wait(2)

            # Selenium Grid Settings
            # For dockerized chrome.
            self._driver = webdriver.Remote(
                command_executor="http://chrome:4444/wd/hub",
                desired_capabilities=DesiredCapabilities.CHROME,
                options=options,
            )

        return self._driver

    def selenium_get(self, url):
        """
        Requests specified url.
        :param url: Requested URL.
        Returns driver's page_source.
        """

        try:
            self.driver.get(url)
            self.logger.info(f"Requesting with selenium: {url}")
            random_sleep_small()
            return self.driver.page_source
        except Exception as e:
            self.logger.error(f"(selenium_get) Exception: {e}")
            return None

    @property
    def url(self):
        return self.driver.current_url

    def parse_response(self, response):
        """
        Parse text response from selenium_get.
        Returns HtmlElement.
        :param response: Text response from GET.
        """

        assert response, self.logger.error(
            "Parsing response failed, received invalid response object."
        )
        try:
            hp = HTMLParser(encoding="utf-8")
            element = fromstring(
                response,
                parser=hp,
            )
            self.logger.debug("Parsing response to HtmlElement.")
            return element
        except Exception as e:
            self.logger.error(f"(parse_response) Exception: {e}")

    def parse_driver_response(self):
        """
        Used with selenium driver current page_source.
        Doesn't need HTMLelement as an input.
        Parses current page and produce a HTMLElement from it.
        """

        try:
            hp = HTMLParser(encoding="utf-8")
            element = fromstring(self.driver.page_source, parser=hp)
            self.logger.debug(
                f"Parsing page to HtmlElement at: {self.driver.current_url}"
            )
            return element
        except Exception as e:
            self.logger.error(f"Error parsing page to HTML: {e}")
            return None

    def do_cleanup(self):
        """
        Delete all cookies and quit Selenium driver.
        """
        if self._driver:
            self.driver.delete_all_cookies()

            self.driver.quit()
            self._driver = None
            self.logger.debug("Driver exited, cookies deleted.")
        else:
            self.logger.info("Driver was already closed.")

    def find_selenium_element(
        self,
        xpath_to_search,
        ignore_not_found_errors=False,
    ):
        """
        Used with Selenium driver.
        Finds element by specified Xpath.
        Return Selenium element to interact with.
        :param ignore_not_found_errors:
            - Can be set to True to not produce error logs,
                when element is not found.
        """
        try:
            element = self.driver.find_element(
                By.XPATH,
                xpath_to_search,
            )
            self.logger.debug(f"(find_selenium_element), returned: {1} element.")
            return element
        except ElementNotVisibleException:
            self.logger.error(f"Selenium element not visible")
            return None
        except NoSuchElementException:
            if ignore_not_found_errors:
                return None
            else:
                self.logger.error(
                    f"(find_selenium_element) Selenium element not found. Is the Xpath ok?"  # noqa
                )
                return None
        except Exception as e:
            self.logger.error(f"(find_selenium_element) exception: {e}")
            return None

    def find_selenium_select_element(
        self,
        xpath_to_search,
        ignore_not_found_errors=False,
    ):
        """
        Used with Selenium driver.
        Find 'select' (drop-down) element by Xpath.
        Return element to interact with.
        - :param ignore_not_found_errors:
            Can be set to True to not produce error logs,
            when element is not found.
        """
        try:
            select_element = Select(
                self.find_selenium_element(
                    xpath_to_search=xpath_to_search,
                    ignore_not_found_errors=ignore_not_found_errors,
                )
            )
            return select_element
        except Exception as e:
            self.logger.error(f"(find_selenium_select_element) exception: {e}")

    def find_selenium_elements(
        self,
        xpath_to_search,
        ignore_not_found_errors=False,
    ):
        """
        Used with Selenium driver.
        Finds elements by specified Xpath.
        Return Selenium web elements to interact with.
         - :param ignore_not_found_errors:
            Can be set to True to not produce error logs,
            when elements are not found.
        """
        try:
            elements = self.driver.find_elements(
                By.XPATH,
                xpath_to_search,
            )
            self.logger.info(
                f"(find_selenium_elements), returned: {len(elements)} elements."  # noqa
            )
            return elements
        except ElementNotVisibleException:
            self.logger.error(f"Selenium element not visible.")
            return None
        except NoSuchElementException:
            if ignore_not_found_errors:
                return None
            else:
                self.logger.error(f"Selenium element not found.")
                return None
        except Exception as e:
            self.logger.error(f"(find_selenium_element) Exception: {e}")
            return None

    def find_all_elements(
        self,
        html_element,
        xpath_to_search,
        ignore_not_found_errors=False,
    ):
        """
        Finds elements by Xpath on given HTMLElement.
        Returns lists of HtmlElements for further processing.
        :param ignore_not_found_errors:
            - Can be set to True to not produce error logs,
                when elements are not found.
        """
        try:
            elements_list = html_element.xpath(xpath_to_search)
            if elements_list:
                self.logger.debug(
                    f"(find_all_elements), returned: {len(elements_list)} elements."  # noqa
                )
                return elements_list
            else:
                if ignore_not_found_errors:
                    return None
                else:
                    self.logger.error(
                        "(find_all_elements) Returned an empty list.",
                    )
                    return None
        except Exception as e:
            self.logger.error(f"(find_all_elements) Some other Exception: {e}")
            return None

    def find_element(
        self,
        html_element,
        xpath_to_search,
        ignore_not_found_errors=False,
    ):
        """
        Find single element/value by Xpath on provided HtmlElement.
        Returns searched value.
        """
        try:
            element = html_element.xpath(xpath_to_search)[0]
            return element
        except IndexError:
            if ignore_not_found_errors:
                return None
            else:
                self.logger.error(
                    "(find_element) Returned an empty list.",
                )
                return None
        except Exception as e:
            self.logger.error(f"(find_element) Some other Exception: {e}")
            return None

    def initialize_html_element(self, selenium_element):
        """
        Used with Selenium driver.
        Initialize a part of content that is loaded on click.
        ::param xpath_to_click::
            - Xpath to element that we have to click to
                load desired element (ie: modal?).
        """
        if isinstance(selenium_element, WebElement):
            try:
                # Yes I know that Selenium click() relies on move_to_element()
                self.scroll_to_element(selenium_element=selenium_element)
                selenium_element.click()
                self.logger.debug("Successfully clicked on specified element.")
                random_sleep_small_l2()
                return True
            except NoSuchElementException:
                self.logger.error(
                    "Failed at finding element to click. Maybe element was already clicked?"  # noqa
                )
                return None
            except ElementClickInterceptedException:
                self.logger.error(
                    f"Failed at clicking element - interception detected. Trying known popups Xpathses..."
                )
                try:
                    self.close_popups_elements_on_error(
                        xpathses_to_search=self.potenial_popups_xpaths
                    )
                    self.scroll_to_element(selenium_element=selenium_element)
                    selenium_element.click()
                    self.logger.debug("Successfully clicked on specified element.")
                    random_sleep_small_l2()
                    return True
                except Exception as ee:
                    self.logger.error(
                        f"(initialize_html_element: ElementClickInterceptedException check) Some other exception: {ee}",  # noqa
                    )
                    return None
            except ElementNotVisibleException:
                self.logger.error(
                    "ELEMENT NOT VISIBLE OCCURRED IMPLEMENT PROPER MECHANIC!"  # noqa
                )
                return None
            except Exception as e:
                self.logger.error(
                    f"(initialize_html_element) Some other Exception: {e}",
                )
                return None
        else:
            self.logger.error(
                "Element is not instance of Selenium's Webelement."  # noqa
            )
            return None

    def if_xpath_in_element(self, html_element, xpath_to_search):
        """
        Looks for single object within provided HTMLElement.
        Returns True is successful.
        """
        try:
            html_element.xpath(xpath_to_search)[0]
            return True
        except IndexError:
            self.logger.debug(
                f"(if_xpath_in_element) Search for: ('{xpath_to_search}') returned an empty list."  # noqa
            )
            return None
        except Exception as e:
            self.logger.error(f"(if_xpath_in_element), Exception: {e}")
            return None

    def send_text_to_element(self, text, selenium_element):
        """
        Takes Selenium Element as an input, sends specified text to it.
        """
        if isinstance(selenium_element, WebElement):
            try:
                self.scroll_to_element(selenium_element=selenium_element)
                selenium_element.clear()
                selenium_element.send_keys(text)
                selenium_element.send_keys(Keys.ENTER)
                random_sleep_small()
                self.logger.info(
                    f"Successfully send text: '{text}' to desired element.",
                )
            except (ElementNotVisibleException, ElementClickInterceptedException):
                # TODO:
                # Add unified logic of reacting to this kind of Exceptions.
                # Like : ElementClickInterceptedException and ElementNotVisibleException.
                # Example: Run check for defined Xpathses,
                #  - of elements that may appear on the website and close them.
                self.logger.error("Specified element is not visible or intercepted.")
            except Exception as e:
                self.logger.error(
                    f"(send_text_to_element) Some other exception: {e}",
                )
        else:
            self.logger.error(
                "Element is not instance of Selenium's Webelement."  # noqa
            )

    def scroll_to_element(self, selenium_element):
        """
        Takes Selenium Element as an input. Scrolls to this element.
        """
        actions = ActionChains(self._driver)
        try:
            actions.move_to_element(selenium_element).perform()
            self.logger.debug(
                f"Successfully scrolled to desired element.",
            )
        except Exception as e:
            self.logger.error(
                f"(scroll_to_element) Some other exception: {e}",
            )

    def find_and_click_selenium_element(self, html_element, xpath_to_search):
        """
        Given the HtmlElement searches for defined Xpath and tries to click it.
        """
        # This check is faster then Selenium's.
        if_banner_in_html = self.if_xpath_in_element(
            html_element=html_element, xpath_to_search=xpath_to_search
        )
        if if_banner_in_html:
            self.logger.info("WebElement found, clicking...")
            try:
                element_click_button = self.find_selenium_element(
                    xpath_to_search=xpath_to_search
                )
                initialized = self.initialize_html_element(
                    selenium_element=element_click_button,
                )
                if initialized:
                    self.logger.info("Successfully clicked WebElement.")
                else:
                    self.logger.error("Failed at clicking WebElement.")
            except Exception as e:
                self.logger.error(
                    f"(find_and_click_selenium_element) Some other exception: {e}"
                )
        else:
            self.logger.info("No WebElement to click, passing...")

    def close_cookies_banner(self, html_element):
        """
        Finds Cookies Policy in provided HtmlElement and closes it.
        Needs self.cookies_close_xpath to work.
        """
        self.find_and_click_selenium_element(
            html_element=html_element,
            xpath_to_search=self.cookies_close_xpath,
        )

    def close_popups_elements_on_error(self, xpathses_to_search):
        """
        Searches list of knows Xpathses for popup elements.
        If element is found, closes it.
        """
        for xpath in xpathses_to_search:
            element = self.find_selenium_element(
                xpath_to_search=xpath, ignore_not_found_errors=True
            )
            if element is not None:
                self.logger.info("Found critical popup element. Closing.")
                element.click()
                random_sleep_small()
            else:
                pass
