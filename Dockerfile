FROM python:3.7-slim
LABEL Maintainer="LRVT"

RUN apt-get update 
RUN apt-get install -y wget gconf-service libasound2 libatk1.0-0 libcairo2 libcups2 libfontconfig1 libgdk-pixbuf2.0-0 libgtk-3-0 libnspr4 libpango-1.0-0 libxss1 fonts-liberation libappindicator1 libnss3 lsb-release xdg-utils

#download and install chrome
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN dpkg -i google-chrome-stable_current_amd64.deb; apt-get -fy install

COPY . /app

RUN mkdir -p /app/results
RUN pip install -r /app/requirements.txt

WORKDIR /app
ENTRYPOINT [ "python", "spidersel.py"]

CMD [ "python", "spidersel.py", "--help"]
