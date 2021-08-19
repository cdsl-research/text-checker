# text-checker

テクニカルレポート(PDF形式)をアップロードすると自動でレビューを行うWebアプリケーション．

![image](https://user-images.githubusercontent.com/2428176/130031892-00b88e06-6a14-4a26-9e4c-d63b27102dc1.png)

## Requirements

- Python v3.7 or later
- Node.js v14 or later

## Usage

1. Create Node.js and Python enviroments.

2. Create venv and Install packages.

```
python -m venv env
. env/bin/activate
pip install -U pip
pip install -r requirements.txt
```

3. Install npm packages.

```
cd textlint/
npm install
```

4. Start uvicorn server.

```
cd ..
uvicorn main:app
```

## Docker image

1. Start a container.
 
```
docker run -d -p 3000:8000 hcr.io/cdsl-research/text-checker
```

2. Access web interface.

```
curl http://127.0.0.1:3000/
```

## Note

Upload a pdf file to web app by curl.

```
curl -X POST -F 'file=@./example.pdf' http://localhost:8000/api/v1/analysis
```

Enable hot reload for dev.

```
uvicorn main:app --reload
```
