# text-checker

テクニカルレポート(PDF形式及びdocx形式)をアップロードすると自動でレビューを行うWebアプリケーションです。
※このWebアプリケーションは日本語の文書にのみ対応しています。

![image](/text-checker.PNG)

## 必要条件

- Python v3.7 または最新版
- Node.js v14 または最新版

## 使い方

1. docker-composeを以下のように実行する。

```
docker-compose up --build
```

初回は--build

2. 以下のアドレスをブラウザに入力し、接続する。

http://localhost:8000/

# Eng.ver
A web application that automatically reviews technical reports (PDF and docx formats) when they are uploaded.
*This web application only supports documents in Japanese.

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

# Note

Upload a pdf file to web app by curl.

```
curl -X POST -F 'file=@./example.pdf' http://localhost:8000/api/v1/analysis
```

Enable hot reload for dev.

```
uvicorn main:app --reload
```
