FROM python:3.10
WORKDIR /usr/src/app

RUN apt-get update && apt-get install -y \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev \
    postgresql-client \
    && apt-get clean

COPY requirements.txt .
COPY wait-for-it.sh /usr/src/app/wait-for-it.sh
RUN pip install -r requirements.txt

