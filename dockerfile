FROM python:3.9.12
RUN mkdir /code
WORKDIR /code

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

COPY ./req.txt /code/

RUN pip install -r req.txt
EXPOSE 8000
COPY . /code/