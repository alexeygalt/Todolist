FROM python:3.10-slim

ENV PYTHONBUFFERED 1
ENV DOCKER_DEFAULT_PLATFORM=linux/amd64
WORKDIR app/
COPY /requirements.txt .
RUN pip install -r requirements.txt
COPY . .

CMD python ./manage.py runserver 0.0.0.0:8000