from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, InvalidSessionIdException, WebDriverException
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import requests
from qa import qa

class LinkScraper:
    """
    LinkScraper is responsible for scraping data from web pages. 
    It uses Selenium WebDriver to navigate and extract required information based on the site configuration.
    """

    def __init__(self, site_config, driver):
        """
        Initializes the LinkScraper with site configuration and Selenium WebDriver.
        """
        self.site_config = site_config
        self.driver = driver
        self.default_timeout = 2
        self.page_load_timeout = 8
        self.skipif_config = site_config.get('skipif', None)

    def visit_and_scrape(self, url):
        """
        Visits a URL and scrapes data from it. Checks for 404 errors before scraping.
        Handles page load timeouts and WebDriver exceptions, attempting to reinitialize the driver if needed.
        """
        if self._is_404_url(url):
            qa(f"URL returned 404: {url}", 'red')
            return {}

        try:
            self._visit(url)
            return self._scrape_data()
        except TimeoutException:
            qa("Skipping scraping due to page load timeout", 'red')
            return {}
        except (InvalidSessionIdException, WebDriverException) as e:
            qa(f"Encountered error: {e}. Reconnecting...", 'red')
            self.driver = self._reinitialize_driver()
            self._visit(url)
            return self._scrape_data()

    def _is_404_url(self, url):
        """
        Checks if the given URL returns a 404 status code.
        """
        try:
            response = requests.head(url, timeout=5)
            return response.status_code == 404
        except requests.RequestException:
            return False

    def _visit(self, url):
        """
        Navigates the WebDriver to the specified URL.
        Sets a timeout for page loading.
        """
        try:
            self.driver.set_page_load_timeout(self.page_load_timeout)
            self.driver.get(url)
        except TimeoutException:
            qa("Timed out waiting for page to load", 'red')
            raise TimeoutException("Page load timeout")

    def _scrape_data(self):
        """
        Scrapes data from the current page based on the site configuration.
        Skips scraping if specified conditions are met (skipif config).
        """
        scraped_data = {}
        if self.skipif_config:
            elements = self.driver.find_elements(By.CSS_SELECTOR, self.skipif_config['selector'])
            if len(elements) > 0:
                return scraped_data

        for config_item in self.site_config["data"]:
            scraped_data.update(self._process_config_item(config_item))

        return scraped_data

    def _process_config_item(self, config_item):
        """
        Processes a single configuration item to extract data from the page.
        Handles different types of selectors and 'try' configurations.
        """
        # ... (rest of the method implementation)
        pass  # placeholder for the rest of the method implementation

    # ... (rest of the class implementation, including other helper methods)

    def _reinitialize_driver(self):
        """
        Reinitializes the WebDriver. Useful when encountering session or WebDriver-related issues.
        """
        options = Options()
        options.add_argument('-headless')
        options.set_preference('permissions.default.image', 2)
        return webdriver.Firefox(options=options)
