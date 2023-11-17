import requests 
from bs4 import BeautifulSoup

class WebScraper:

    def __init__(self):
        self.session = requests.Session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        self.session.headers.update(self.headers)

    def scrape_data(self, url, selector_objects, headers=None):
        # Update headers if provided
        if headers:
            self.session.headers.update(headers)
        
        response = self.session.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors

        soup = BeautifulSoup(response.content, 'html.parser')
            
        scraped_data = {}

        for obj in selector_objects:
            title = obj["title"]
            selector = obj["selector"]
            target = obj.get("target", "innerText")
            element = soup.select_one(selector)

            if target == "innerText":
                scraped_data[title] = element.get_text() if element else ''
            elif target == "innerHTML":
                scraped_data[title] = str(element) if element else ''
            else:  # For other attributes like 'src'
                scraped_data[title] = element[target] if element else ''

        return scraped_data
