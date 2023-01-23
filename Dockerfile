FROM python:3.9-slim-buster AS build

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# RUN python -m venv env

# ENV PATH="/app/env/bin:$PATH"

# RUN . env/bin/activate
RUN apt-get update && apt-get install wget unzip zip -y

RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN dpkg -i google-chrome-stable_current_amd64.deb; apt-get -fy install

COPY requirements.txt requirements.txt

RUN wget -O LATEST_RELEASE chromedriver.storage.googleapis.com/LATEST_RELEASE && export latest=$(cat LATEST_RELEASE) && sed -i "s/LTS/$latest/g" requirements.txt  

RUN pip install -r requirements.txt

# COPY chromedriver.exe /usr/local/bin/chromedriver.exe

COPY . /app/

RUN export PATH=$PATH:`chromedriver-path`

# ENTRYPOINT ["/bin/sleep","3600"]

CMD [ "python", "-m" , "flask", "--app", "./flask-docker/flaskui", "run", "--host=0.0.0.0"]

# CMD [ "python3", "-m" , "flask", "-app", "flaskui", "run"]

# FROM python:3.9-slim-buster

# ENV PYTHONUNBUFFERED=1
# ENV PYTHONDONTWRITEBYTECODE=1

# WORKDIR /flask-docker

# COPY --from=build /flask-docker /flask-docker

# COPY . .

# EXPOSE 5000

# ENV PATH="/flask-docker/env/bin:$PATH"

# RUN . env/bin/activate

# ENTRYPOINT ["/bin/sleep","3600"]

