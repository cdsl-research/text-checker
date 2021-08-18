FROM debian:buster-slim

COPY . /work
WORKDIR /work/textlint
RUN apt-get -y update && \
    apt-get -y install curl python3 python3-pip nodejs npm && \
    npm install && \
    apt-get -y  install build-essential libssl-dev libffi-dev python3-dev cargo

WORKDIR /work
RUN pip3 install --upgrade pip && \
    pip3 install -r requirements.txt

CMD ["uvicorn", "main:app"]
