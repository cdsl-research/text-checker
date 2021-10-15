FROM python:3.9-buster
COPY . /work
WORKDIR /work
RUN pip3 install --upgrade pip && \
    pip3 install -r requirements.txt

ENTRYPOINT ["uvicorn"]
CMD ["main:app", "--host", "0.0.0.0"]
