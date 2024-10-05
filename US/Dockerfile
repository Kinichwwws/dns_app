FROM ubuntu:latest
FROM python:3.12
LABEL authors="shuqianwen"

WORKDIR /usr/src/app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

CMD ["python", "user_server.py"]