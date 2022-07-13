FROM python:3.8
RUN apt-get update && apt-get install
RUN python -m pip install --upgrade pip

ENV PYTHONUNBUFFERED=1
RUN mkdir /vending_machine
WORKDIR /vending_machine/
COPY requirements.txt /vending_machine/
RUN python -m pip install -r requirements.txt
COPY . /vending_machine/