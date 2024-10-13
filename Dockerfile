FROM python
WORKDIR /usr/src/app
COPY requirenments.txt ./
RUN pip install -r requirements.txt