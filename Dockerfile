FROM python:3.9

ENV PYTHONUNBUFFERED 1

RUN mkdir /inventory_manager

WORKDIR /inventory_manager

ADD . /inventory_manager/

RUN pip install -r requirements.txt

