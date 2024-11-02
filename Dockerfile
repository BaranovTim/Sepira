FROM python:3.10
WORKDIR /usr/src/app

RUN apt-get update && apt-get install -y \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev \
    zbar-tools \
    && apt-get clean \

CMD ["sh", "-c", "wait-for-it pgdb:5432 -- python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]

COPY requirements.txt .
RUN pip install -r requirements.txt

