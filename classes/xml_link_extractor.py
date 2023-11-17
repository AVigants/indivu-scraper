import requests
from xml.etree import ElementTree as ET

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

class XMLLinkExtractor:
    
    def __init__(self, url):
        self.url = url
        
    def fetch_links(self):
        try:
            response = requests.get(self.url, headers=headers)
            response.raise_for_status()  # Raise an exception for HTTP errors

            # Parse the XML content.
            tree = ET.fromstring(response.content)

            # The links are usually in the <loc> tags.
            namespaces = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
            links = [elem.text for elem in tree.findall(".//sm:loc", namespaces=namespaces)]
            
            return links

        except requests.exceptions.RequestException as e:
            print(f"Error fetching URL {self.url}: {e}")
            return []  # Return an empty list in case of error
