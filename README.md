# SpiderSel
Python 3 script to crawl and spider websites for keywords via selenium.

## 🎓 Usage

````bash
usage: spidersel.py [-h] [--url URL] [--depth DEPTH] [--min-length MIN_LENGTH]

Web Crawler and Keyword Extractor

options:
  -h, --help                  show this help message and exit
  --url URL                   URL of the website to crawl
  --depth DEPTH               Depth of spidering (number of subpages to visit) (default: 1)
  --min-length MIN_LENGTH     Minimum keyword length (default: 4)
````

## 🐳 Example 1 - Docker Run

### External Dockerhub Image

````
docker run -v ${PWD}:/app/results --rm l4rm4nd/spidersel:latest --url https://www.apple.com
````

You will find your scan results in the current directory.

### Local Docker Build Image

If you don't trust my image on Dockerhub, please go ahead and build the image yourself:

````
git clone https://github.com/Haxxnet/SpiderSel && cd SpiderSel
docker build -t spidersel .
docker run -v ${PWD}:/app/results --rm spidersel --url https:/www.apple.com
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
python3 spidersel.py --url https://www.apple.com/
````

The extracted keywords will be stored in an output file within the results folder.
