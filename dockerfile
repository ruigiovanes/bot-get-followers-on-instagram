FROM python:latest as base

RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'

RUN apt-get -y update
RUN apt-get install -y google-chrome-stable

RUN mkdir /work/
WORKDIR /work/

COPY src/requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY ./src/ /work/

WORKDIR /home
RUN mkdir /home/application/

COPY ./driver/ /home/application/driver/

FROM base as debug
RUN pip install ptvsd

ENV DOCKER_CONTAINER Yes

WORKDIR /work/
CMD python -m ptvsd --host 0.0.0.0 --port 5678 --wait app.py