FROM debian:buster-slim

COPY . /work
WORKDIR /work/textlint
RUN apt-get -y update && \
    apt-get -y install rust libffi-dev python3 python3-pip nodejs npm && \
    npm install

WORKDIR /work
RUN pip3 install -r requirements.txt

CMD ["uvicorn", "main:app"]
