import httpx
from scraper.helpers.logger import logger
from scraper.helpers.randoms import get_random_user_agent
from scraper.options.settings import USER_AGENTS


class ValidationCrawler:
    """
    Simple crawler used for validating pages for status codes before starting Selenium scraper.
    """

    def __init__(self, logger=logger):
        self.logger = logger

    @property
    def user_agent(self):
        agent = get_random_user_agent(USER_AGENTS)
        return agent

    def python_get(self, url):
        """
        Requests specified url.
        :param url: Requested URL.
        Returns Response's status code.
        Used for validating Pages.
        """
        headers = {"user-agent": f"{self.user_agent}"}
        try:
            response = httpx.get(url, headers=headers, timeout=10)
            return response.status_code
        except Exception as e:
            self.logger.error(f"(python_get) Exception: {e}")
            return None

    def validate_page_status(self, url):
        """
        Validates page for anything except critcal status codes.
        """
        # TODO:
        # Add dicionary of accepted status code (or not accepted)
        # Change if check for status logic.
        status_code = self.python_get(url=url)

        if status_code is not None:
            if status_code != 404:
                self.logger.info(
                    f"Validation check for {url} returned valid status code: {status_code} - Proceeding..."
                )
                return True
            else:
                self.logger.info(
                    f"Validation check for {url} returned invalid status code: {status_code} - Quiting."
                )
                return False
        else:
            self.logger.info(f"Requesting {url} failed. Quiting.")
            return False
