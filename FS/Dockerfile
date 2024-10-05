FROM ubuntu:latest
FROM python:3.12
LABEL authors="shuqianwen"

WORKDIR /usr/src/app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 9090

CMD ["python", "fibonacci_server.py"]