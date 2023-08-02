FROM infologistix/docker-selenium-python:alpine
LABEL Maintainer="LRVT"

WORKDIR /app
COPY requirements.txt /app
COPY spidersel.py /app

RUN pip install --no-cache-dir -r /app/requirements.txt && \
    mkdir -p /app/results

ENTRYPOINT [ "python3", "spidersel.py"]
CMD [ "python3", "spidersel.py", "--help"]
