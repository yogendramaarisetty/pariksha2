FROM ubuntu
ENV PYTHONUNBUFFERED=1
WORKDIR /usr/src/app
RUN apt-get update && apt-get install -y openjdk-8-jdk
RUN apt update && apt install -y python3-pip
COPY requirements.txt ./
RUN pip3 install -r requirements.txt