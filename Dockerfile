FROM python:3.9-slim-buster AS build

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

RUN apt-get update && apt-get install wget unzip zip -y && apt-get clean

RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN dpkg -i google-chrome-stable_current_amd64.deb; apt-get -fy install

COPY requirements.txt requirements.txt

RUN wget -O LATEST_RELEASE chromedriver.storage.googleapis.com/LATEST_RELEASE && export latest=$(cat LATEST_RELEASE) && sed -i "s/LTS/$latest/g" requirements.txt  

RUN rm google-chrome-stable_current_amd64.deb

RUN pip install -r requirements.txt

COPY . /app/

CMD [ "python", "-m" , "flask", "--app", "flaskui", "run", "--host=0.0.0.0"]

# CMD [ "python3", "-m" , "flask", "-app", "flaskui", "run"]

# FROM python:3.9-slim-buster

# ENV PYTHONUNBUFFERED=1
# ENV PYTHONDONTWRITEBYTECODE=1

# WORKDIR /app

# # RUN apt-get update && apt-get clean

# RUN apt-get install -y libglib2.0-0 libnss3 libgconf-2-4 libfontconfig1 && apt-get clean

# COPY --from=build /app /app

# RUN dpkg -i google-chrome-stable_current_amd64.deb; apt-get -fy install

# RUN export latest=$(cat LATEST_RELEASE) && sed -i "s/LTS/$latest/g" requirements.txt

# RUN pip install -r requirements.txt

# RUN export PATH=$PATH:`chromedriver-path`

# RUN rm google-chrome-stable_current_amd64.deb

# EXPOSE 5000




