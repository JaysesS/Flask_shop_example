FROM python:3.6.9

WORKDIR /app

ADD . /app

RUN python3 -m pip install -r requirements.txt

CMD ["uwsgi", "app.ini"]