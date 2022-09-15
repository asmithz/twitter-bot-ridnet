FROM python:3.8.13-slim

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN python3.8 -m pip install --no-cache-dir -r /app/requirements.txt 

COPY ./twitter_bot /app/twitter_bot

CMD ["python3.8", "-u", "twitter_bot/main.py"]