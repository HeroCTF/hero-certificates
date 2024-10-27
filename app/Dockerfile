FROM python:3.11-slim-buster

WORKDIR /app

COPY . .
RUN pip3 install -r requirements.txt

EXPOSE $LISTEN_PORT
CMD [ "python3", "app.py"]