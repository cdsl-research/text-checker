FROM debian:buster-slim

COPY . /work
WORKDIR /work/textlint
RUN apt-get -y update && \
    apt-get -y install curl libffi-dev libssl-dev python3 python3-pip nodejs npm && \
    npm install && \
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y && \
    export PATH="$PATH:$HOME/.cargo/bin"

WORKDIR /work
RUN pip3 install -r requirements.txt

CMD ["uvicorn", "main:app"]
