# text-checker

テクニカルレポート(PDF形式)をアップロードすると自動でレビューを行うWebアプリケーション．

![image](https://user-images.githubusercontent.com/2428176/130031892-00b88e06-6a14-4a26-9e4c-d63b27102dc1.png)

## Requirements

- Python v3.7 or later
- Node.js v14 or later

## Usage

1. Run docker-compose

```
docker-compose up --build
```

2. Access front service

http://localhost:8000/

## Note

Upload a pdf file to web app by curl.

```
curl -X POST -F 'file=@./example.pdf' http://localhost:8000/api/v1/analysis
```

Enable hot reload for dev.

```
uvicorn main:app --reload
```
