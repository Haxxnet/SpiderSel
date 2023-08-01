'''
Author: LRVT - https://github.com/l4rm4nd
Desc: Python 3 script to crawl and spider websites for keywords via selenium
Version: v1.0
'''

import argparse
import re, os
import string
from bs4 import BeautifulSoup
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from urllib.parse import urljoin, urlparse
import tldextract

# Function to extract keywords from a web page
def extract_keywords(page_content, min_length):
    soup = BeautifulSoup(page_content, 'html.parser')
    keywords = set()
    for text in soup.stripped_strings:
        words = text.split()
        for word in words:
            word = remove_special_characters(word)
            if len(word) >= min_length:
                keywords.add(word.lower())
    return list(keywords)

def remove_special_characters(input_string):
    # Define the regular expression pattern to match special characters
    # Not followed by valid characters (alphanumeric or hyphen)
    pattern = r'[^\w-]|(?<!\w)-(?!\w)'
    # Replace special characters with an empty string
    cleaned_string = re.sub(pattern, '', input_string)
    return cleaned_string

# Function to spider links within the website
def spider_links(driver, base_url, depth, visited_urls, min_length):
    if depth <= 0:
        return []

    driver.get(base_url)
    page_content = driver.page_source
    keywords = extract_keywords(page_content, min_length)
    print(f"[i] Spidering website {base_url}")

    combined_keywords = keywords.copy()
    soup = BeautifulSoup(page_content, 'html.parser')
    for link in soup.find_all('a', href=True):
        absolute_url = urljoin(base_url, link['href'])
        parsed_url = urlparse(absolute_url)
        if parsed_url.netloc == urlparse(base_url).netloc and absolute_url not in visited_urls:
            visited_urls.add(absolute_url)
            subpage_keywords = spider_links(driver, absolute_url, depth - 1, visited_urls, min_length)
            combined_keywords.extend(subpage_keywords)

    return combined_keywords

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Web Crawler and Keyword Extractor")
    parser.add_argument("--url", required=True, type=str, help="URL of the website to crawl")
    parser.add_argument("--depth", required=False, default=1, type=int, help="Depth of spidering (number of subpages to visit) (default: 1)")
    parser.add_argument("--min-length", required=False, type=int, default=4, help="Minimum keyword length (default: 4)")
    args = parser.parse_args()

    # Create output folder
    try:
       os.mkdir("results")
    except Exception as e:
       pass

    # Headless browser setup with Selenium
    # Specify the path to the ChromeDriver executable
    chrome_driver_path = "/usr/bin/chromedriver"

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument("--disable-setuid-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=chrome_options)

    # Start spidering from the provided URL
    visited_urls = set()
    visited_urls.add(args.url)
    keywords = spider_links(driver, args.url, args.depth, visited_urls, args.min_length)
    unique_keywords = list(set(keywords))

    # Close the browser after spidering is done
    driver.quit()

    # Combine keywords from all spidered sites and print them as newline-separated values
    combined_keywords = '\n'.join(unique_keywords)
    keyword_list = combined_keywords.split('\n')
    num_keywords = len(keyword_list)

    # Get the root domain from the URL
    extracted = tldextract.extract(args.url)
    
    if extracted.subdomain:
        fqdn = f"{extracted.subdomain}.{extracted.domain}.{extracted.suffix}"
    else:
        fqdn = f"{extracted.domain}.{extracted.suffix}"

    # Get the current date and time in the specified format
    current_datetime = datetime.now().strftime("%Y%m%d%H%M%S")
    # Create the output filename
    output_filename = f"{fqdn}_{current_datetime}.txt"

    # Write the keywords to the output file
    with open("results/" + output_filename, 'w') as file:
        file.write(combined_keywords)

    print()
    print(f"[i] Crawled {num_keywords} keywords.")
    print(f"[i] Keywords have been written to {output_filename}. Enjoy!")
