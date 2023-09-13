<div align="center" width="100%">
    <h1>🕷️ SpiderSel 🕷️</h1>
    <p>Python 3 script to crawl and spider websites for keywords via selenium</p><p>
    <a target="_blank" href="https://github.com/l4rm4nd"><img src="https://img.shields.io/badge/maintainer-LRVT-orange" /></a>
    <a target="_blank" href="https://hub.docker.com/repository/docker/l4rm4nd/spidersel/general"><img src="https://badgen.net/badge/icon/l4rm4nd%2Fspidersel:latest?icon=docker&label" /></a><br>
    <!--<a target="_blank" href="#"><img src="https://ForTheBadge.com/images/badges/makes-people-smile.svg" /></a><br>-->
    <a href="https://www.buymeacoffee.com/LRVT" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy Me A Coffee" style="height: 41px !important;width: 174px !important;box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;-webkit-box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;" ></a>
</div>

## 💎 Features

SpiderSel provides the following features:

- Crawling of HTTP and HTTPS websites for keywords via Selenium (native JS support)
- Spidering of new URLs found within source code (adjustable depth, stays samesite)
- Filtering keywords by length and removing non-sense (paths, emails, protocol handlers etc.)
- Storing keywords into a separate results directory (txt file)

Basically alike to [CeWL](https://github.com/digininja/CeWL) or [CeWLeR](https://github.com/roys/cewler) but with support for websites that require JavaScript.

## 🎓 Usage

````bash
usage: spidersel.py [-h] --url URL [--depth DEPTH] [--min-length MIN_LENGTH]

Web Crawler and Keyword Extractor

options:
  -h, --help                  show this help message and exit
  --url URL                   URL of the website to crawl
  --depth DEPTH               Depth of subpage spidering (default: 1)
  --min-length MIN_LENGTH     Minimum keyword length (default: 4)
  --lowercase                 Convert all keywords to lowercase
  --include-emails            Include emails as keywords
````

## 🐳 Example 1 - Docker Run

### External Dockerhub Image

````
docker run -v ${PWD}:/app/results --rm l4rm4nd/spidersel:latest --url https://www.apple.com --lowercase --include-emails
````

You will find your scan results in the current directory.

### Local Docker Build Image

If you don't trust my image on Dockerhub, please go ahead and build the image yourself:

````
git clone https://github.com/Haxxnet/SpiderSel && cd SpiderSel
docker build -t spidersel .
docker run -v ${PWD}:/app/results --rm spidersel --url https:/www.apple.com --lowercase --include-emails
````

## 🐍 Example 2 - Native Python

### Installation

````bash
# clone repository and change directory
git clone https://github.com/Haxxnet/SpiderSel && cd SpiderSel

# optionally install google-chrome if not available yet
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb

# install python dependencies; optionally use a virtual environment (e.g. virtualenv, pipenv, etc.)
pip3 install -r requirements.txt
````

### Running

````
python3 spidersel.py --url https://www.apple.com/ --lowercase --include-emails
````

The extracted keywords will be stored in an output file within the results folder.
