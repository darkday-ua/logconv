FROM python:3.9.5-slim
ENV DOCKER=YES
RUN apt update
RUN apt install git -y
WORKDIR /usr/src/app

COPY ./logconv.py .
COPY ./example.log .

ENTRYPOINT ["python", "logconv.py"]
