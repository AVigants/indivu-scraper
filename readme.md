# INDIVU data scraper


#### Description
This program is designed for web scraping, specifically tailored for extracting data from XML sitemaps of various websites. It uses Selenium with Python for navigating and extracting data from web pages. The program is configured to scrape data from websites like Wolt, Barbora, and Rimi as per the provided `config.json` file.

#### Capabilities
- **Fetching XML Links**: Extracts all links from specified XML sitemaps.
- **Data Scraping**: Visits each link and scrapes data based on specified CSS selectors in `config.json`.
- **Data Handling**: Handles scraped data, including checking for 404 errors and scraping specific data points (like product names, prices, images, etc.).
- **BigQuery Integration**: Includes functionality to write scraped data to Google BigQuery.
- **History Tracking**: Maintains a history of visited links to avoid re-scraping.

#### How to Use
1. **Set Up Selenium Webdriver**:
- Download Chrome webdriver and add it to the `webdrivers` folder.
     [Chrome Webdriver Download](https://chromedriver.chromium.org/downloads)

2. **Create and Activate a Virtual Environment**:
   ```bash
   $ python -m venv myenv
   $ source myenv/bin/activate
   ``````

3. **Install the required packages**:

    ```bash
    $ pip install selenium
    ```

4. **Run the program**:

- Modify config.json as per your scraping needs.
- Execute main.py to start the scraping process.


### **Potential improvements**:


- Multi-Threading: Implement multi-threading to enhance the scraping speed by processing multiple links simultaneously.
- Rotating Proxies: Use rotating proxies to avoid IP bans and simulate organic traffic.
- Local Data Storage: Save scraped data locally in ndjson files for better data management and offline access.
- Error Handling Enhancements: Improve error handling mechanisms for more robust and fail-safe operations.
- User-Agent Randomization: Randomize user-agents to further avoid detection by web servers.
- Headless Browser Options: Provide an option to run the scraper in headless mode for better performance on servers.
- Logging System: Implement a logging system for better tracking of the scraping process and debugging.
