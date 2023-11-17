# ---- Imports ----
import json
import os
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from xml_link_extractor import XMLLinkExtractor
from link_scraper import LinkScraper
from bq import BigQueryWriter
from qa import qa

# --- General Functions ----
def load_or_create_output_file(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            content = f.read()
            return json.loads(content) if content else []
    else:
        with open(filename, 'w') as f:
            json.dump([], f)
        return []

def load_history_links(site_name):
    history_file = site_name + "_history.txt"
    if os.path.exists(history_file):
        with open(history_file, 'r') as f:
            return f.read().splitlines()
    return []

# ---- Initialization ----
qa('init')

options = Options()
options.add_argument('-headless')
options.set_preference('permissions.default.image', 2)
driver = webdriver.Firefox(options=options)
# Init bigQuery writer
bq_writer = BigQueryWriter("bq-service-acc-key.json")

# Read configuration
qa('reading config.json...')

with open('config.json', 'r') as f:
    config = json.load(f)
# ---- MAIN ----
for site_config in config:

    # Fetch all XML links
    qa('fetching XMLs...')
    all_links_set = set()
    for XML in site_config['XMLs']:
        extractor = XMLLinkExtractor(XML)
        fetched_links = extractor.fetch_links()
        all_links_set.update(fetched_links)
    all_links = list(all_links_set)
    qa(f'total unique XML links fetched: {len(all_links)}', 'blue')


    # # Read {{site}}_output.json (only needed if we don't write to BQ)
    # output_file = site_config["site"] + "_output.json"
    # scraped_links_data = load_or_create_output_file(output_file)
    
    # Read {{site}}_history.txt and ignore already visited links:
    history_links = load_history_links(site_config["site"])
    original_link_count = len(all_links)
    all_links = [link for link in all_links if link not in history_links and
                 not ('rimi.lv' in link and ('beauty-and-hygiene' in link or 'house-garden-and-leisure' in link or 'babies-and-children' in link or 'detergents-and-cleaning-supplies' in link or 'back-to-school' in link or 'office-supplies' in link or 'products/pets' in link)) and
                 not ('wolt.com' in link and 'restaurant' not in link)]

    purged_links_count = original_link_count - len(all_links)
    qa(f'total XML links purged: {purged_links_count}', 'red')
    qa(f'total unique XML links remaining: {len(all_links)}', 'green')


    # Scrape links
    scraper = LinkScraper(site_config, driver)
    for i in range(len(all_links)):
        link = all_links[i]
        
        # Scrape data
        start_time = time.time()
        qa(f"Visiting {link}")
        scraped_data = scraper.visit_and_scrape(link)
        time_spent = time.time() - start_time

        # update history.txt file
        with open(site_config["site"] + "_history.txt", 'a') as history:
            history.write(link + "\n")

        # push data to database
        if scraped_data:
            dataset_name = "indivu"
            table_name = site_config["site"]
            bq_writer.write_data(dataset_name, table_name, [{'link': link, 'data': scraped_data}])

        qa(f"{i}/{len(all_links)} \tTime spent: {time_spent}", 'green')

# ---- Program End ----
qa("end")
driver.quit()
