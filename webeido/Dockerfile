FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8-slim
LABEL authors="Nathan Sheffield"

COPY webeido /app/
COPY requirements/requirements-all.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install https://github.com/pepkit/peppy/archive/dev.zip
RUN pip install https://github.com/pepkit/eido/archive/dev.zip
