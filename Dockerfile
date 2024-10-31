FROM python:3.12

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt

RUN mkdir -p config

VOLUME /app/config

ENV PYTHONUNBUFFERED=1

CMD [ "python", "app.py" ]