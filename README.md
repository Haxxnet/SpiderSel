# SpiderSel
Python 3 script to crawl and spider websites for keywords via selenium.

## 🎓 Usage

````bash
usage: spidersel.py [-h] [--url URL] [--depth DEPTH] [--min-length MIN_LENGTH]

Web Crawler and Keyword Extractor

options:
  -h, --help            show this help message and exit
  --url URL             URL of the website to crawl
  --depth DEPTH         Depth of spidering (number of subpages to visit) (default: 3)
  --min-length MIN_LENGTH
                        Minimum keyword length (default: 4)
````

## 🐍 Example 1 - Native Python

### Installation

````bash
# clone repository and change directory
git clone https://github.com/Haxxnet/SpiderSel && cd SpiderSel

# install python dependencies; optionally use a virtual environment (e.g. virtualenv, pipenv, etc.)
pip3 install -r requirements.txt
````

### Running

````
python3 spidersel.py --url https://www.apple.com/ --min-length 7
````

The extracted keywords will be stored in an output file.