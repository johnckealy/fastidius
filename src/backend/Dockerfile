FROM python:3.9

RUN apt-get update && apt-get -y install \
    netcat-openbsd apt-utils

RUN pip install --upgrade pip
RUN mkdir /ubuntu

RUN useradd -ms /bin/bash ubuntu
USER ubuntu
ENV PATH="/home/ubuntu/.local/bin:${PATH}"


COPY --chown=ubuntu:ubuntu requirements.txt /ubuntu/
WORKDIR /ubuntu

RUN pip install -r requirements.txt

COPY --chown=ubuntu:ubuntu . /ubuntu
