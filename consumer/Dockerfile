FROM python:3.9-slim

WORKDIR /app

COPY . /app

RUN pip3 install kafka-python

CMD ["python", "consumer.py"]
