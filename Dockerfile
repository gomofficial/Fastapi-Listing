FROM python:3.10.10

RUN mkdir /app
WORKDIR /app


ENV PYTHONDONTWRITEBYTECODE 1
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONUNBUFFERED 1


COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . /app
EXPOSE 8000