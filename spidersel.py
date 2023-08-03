'''
Author: LRVT - https://github.com/l4rm4nd
Desc: Python 3 script to crawl and spider websites for keywords via selenium
Version: v1.0
'''
import argparse
import re, os, sys
from datetime import datetime
from urllib.parse import urljoin, urlparse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import tldextract

# Function to extract keywords from a web page
def extract_keywords(page_content, min_length):
    soup = BeautifulSoup(page_content, 'html.parser')
    keywords = set()
    for text in soup.stripped_strings:
        words = text.split()
        for word in words:
            word = clean_words(word)
            if len(word) >= min_length:
                keywords.add(word.lower())
    return list(keywords)

def is_url(input_string):
    # Regular expression pattern to match a URL
    url_prefixes = ["https://", "http://", "ftp://", "ftps://", "mailto://", "unix://"]
    return any(input_string.startswith(prefix) for prefix in url_prefixes)

def is_email(input_string):
    # Regular expression pattern to match an email address
    email_pattern = r'^[\w.-]+@[a-zA-Z]+\.[a-zA-Z]{2,}$'
    return re.match(email_pattern, input_string) is not None

def is_weird_keyword(string):
    # Define a regex pattern to check for special characters like _, /, and other symbols
    special_chars_pattern = r"[\W_]+"

    # Define a regex pattern to check for URLs and paths
    url_or_path_pattern = r"^(?:\w+:\/\/|\/).*$"

    # Check if the string contains special characters
    has_special_chars = bool(re.search(special_chars_pattern, string))

    # Check if the string matches the URL or path pattern
    is_url_or_path = bool(re.match(url_or_path_pattern, string))

    # Determine if the string is a common word or a weird URL or path
    if not has_special_chars and not is_url_or_path:
        return False  # normal keyword
    return True  # weird keyword, do not add

def clean_words(input_string):
    if is_url(input_string) or is_email(input_string) or is_weird_keyword(input_string):
        return ""
    return input_string

# Function to spider links within the website
def spider_links(driver, base_url, depth, visited_urls, min_length):
    if depth <= 0:
        return []

    print(f"[task] Spidering {base_url}")
    driver.get(base_url)
    page_content = driver.page_source
    keywords = extract_keywords(page_content, min_length)

    visited_urls.add(base_url)
    
    combined_keywords = keywords.copy()
    soup = BeautifulSoup(page_content, 'html.parser')
    for link in soup.find_all('a', href=True):
        absolute_url = urljoin(base_url, link['href'])
        parsed_url = urlparse(absolute_url)
        if parsed_url.netloc == urlparse(base_url).netloc:
            if absolute_url not in visited_urls:
                subpage_keywords = spider_links(driver, absolute_url, depth - 1, visited_urls, min_length)
                combined_keywords.extend(subpage_keywords)

    return combined_keywords

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Web Crawler and Keyword Extractor")
    parser.add_argument("--url", required=True, type=str, help="URL of the website to crawl")
    parser.add_argument("--depth", required=False, default=1, type=int, help="Depth of subpage spidering (default: 1)")
    parser.add_argument("--min-length", required=False, type=int, default=4, help="Minimum keyword length (default: 4)")
    args = parser.parse_args()

    # Create output folder
    try:
        os.mkdir("results")
    except PermissionError as e:
        print("[x] Permission denied. Unable to create the directory 'results'.")
        sys.exit(0)
    except FileExistsError as e:
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
    keywords = spider_links(driver, args.url, args.depth+1, visited_urls, args.min_length)
    unique_keywords = list(set(keywords))

    # Close the browser after spidering is done
    driver.quit()

    # Combine keywords from all spidered sites and print them as newline-separated values
    combined_keywords = '\n'.join(unique_keywords)
    keyword_list = combined_keywords.split('\n')
    num_keywords = len(keyword_list) - 1

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
    with open("results/" + output_filename, 'w', encoding="utf-8") as file:
        file.write(combined_keywords)
    
    print()
    print(f"[info] Keywords crawled: {num_keywords}")
    print(f"[info] Keywords outfile: {output_filename}")
