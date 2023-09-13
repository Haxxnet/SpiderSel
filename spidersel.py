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


ignored_words = set()
# Function to extract keywords from a web page
def extract_keywords(page_content, min_length):
    soup = BeautifulSoup(page_content, 'html.parser')
    keywords = set()
    for text in soup.stripped_strings:
        words = text.split()
        for word in words:
            pattern = r'^[^a-zA-Z0-9]+|[^a-zA-Z0-9]+$'
            word = re.sub(pattern, '', word)
            word = clean_words(word)
            if len(word) >= min_length:
                if args.lowercase:
                    keywords.add(word.lower())
                else:
                    keywords.add(word)
    return list(keywords)

def is_url(input_string):
    # Regular expression pattern to match a URL
    url_prefixes = ["https://", "http://", "ftp://", "ftps://", "mailto://", "unix://"]
    return any(input_string.startswith(prefix) for prefix in url_prefixes)

def is_email(input_string):
    # Regular expression pattern to match an email address
    email_pattern = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    return re.fullmatch(email_pattern, input_string) is not None

def filter_keywords(keywords):
    filtered_keywords = []
    split_pattern = r'[^a-zA-Z0-9äüö]+'
    email_pattern = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')

    for keyword in keywords:
        # when keyword is an email, add to list before being split
        if re.fullmatch(email_pattern, keyword) is not None:
            filtered_keywords.append(keyword)

        # if word can be splitted, add full keyword to ignored_words first
        if re.search(split_pattern, keyword):
            ignored_words.add(keyword)
            
        # Split by special characters
        for word in re.split(split_pattern, keyword):
            # Ignore empty strings
            if not word:
                ignored_words.add(word)
                continue

            # filter keywords < min_length
            if args.min_length:
                minlength = args.min_length
            else:
                minlength = 4

            if len(word) < minlength:
                continue

            filtered_keywords.append(word)
    
    return filtered_keywords 

def clean_words(input_string):
    if args.include_emails:
        if is_url(input_string):
            ignored_words.add(input_string)
            return ""
        return input_string
    else:
        if is_url(input_string) or is_email(input_string):
        #if is_url(input_string) or is_weird_keyword(input_string):
            ignored_words.add(input_string)
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
    parser.add_argument("--lowercase", help="Convert all keywords to lowercase", required=False, action='store_true')
    parser.add_argument("--include-emails", help="Include emails as keywords", required=False, action='store_true')
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
    #chrome_driver_path = "/usr/bin/chromedriver"

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
    unique_keywords = list(set(filter_keywords(unique_keywords)))

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
    output_ignore_filename = f"{fqdn}_{current_datetime}_ignored_words.txt"

    # Write the keywords to the output file
    with open("results/" + output_filename, 'w', encoding="utf-8") as file:
        file.write(combined_keywords)

    # Write ignored keywords into outfile too
    with open("results/" + output_ignore_filename, 'w', encoding="utf-8") as file:
        unique_ignored_words = list(set(ignored_words))
        unique_ignored_words = '\n'.join(unique_ignored_words)
        file.write(unique_ignored_words)
    
    print()
    print(f"[info] Keywords crawled: {num_keywords}")
    print(f"[info] Keywords outfile: {output_filename}")
    print(f"[info] Keywords ignored: {output_ignore_filename}")
