FROM python:3.9-slim-buster AS build

WORKDIR /app

RUN python -m venv /opt/venv
# Enable venv
ENV PATH="/opt/venv/bin:$PATH"

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

RUN apt-get update && apt-get install wget unzip zip -y

RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . /app/

# ENTRYPOINT ["/bin/sleep","3600"]

FROM python:3.9-slim-buster as app

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Needed for chrome-driver
RUN apt-get update 

WORKDIR /app

COPY --from=build /opt/venv /opt/venv

# Enable venv
ENV PATH="/opt/venv/bin:$PATH"

COPY --from=build /app /app

RUN dpkg -i google-chrome-stable_current_amd64.deb; apt-get -fy install

RUN rm google-chrome-stable_current_amd64.deb

EXPOSE 5000

# CMD ["/bin/sleep","3600"]

# CMD [ "python", "./flaskui.py"]
CMD exec gunicorn --bind :8080 --workers 1 --threads 8 --timeout 0 flaskui:app


