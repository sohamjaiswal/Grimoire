FROM python:3.12.1-alpine3.19

# install gcc
RUN apk add --no-cache gcc musl-dev linux-headers libffi libffi-dev openssl-dev

RUN pip install poetry==1.7.1

# get logs for async stuff 
ENV PYTHONUNBUFFERED 1 

WORKDIR /app
COPY ../../bot/pyproject.toml ./
COPY ../../bot/poetry.lock ./


# CMD poetry install;poetry run python -m pymon bot
CMD poetry install;poetry run dev
