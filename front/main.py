from cgitb import text
from curses import raw
from fileinput import filename
from pydoc import doc
from fastapi import FastAPI
from fastapi import Request
from fastapi import File
from fastapi import UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from docx import Document
import io

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def top(request: Request):
    return templates.TemplateResponse("top.html", {"request": request})


@app.post("/api/v1/analysis")
async def upload(file: UploadFile = File(...)):
    import pdf_to_text
    raw_text = ''
    if ".pdf" in file.filename:

        raw_text = pdf_to_text.pdf_to_text(file.file)
        print("raw_text:", raw_text)
        print("this is PDF file")
        print(file.filename)
    elif ".docx" in file.filename:
        document = Document(io.BytesIO(await file.read()))
        for para in document.paragraphs:
            raw_text += para.text
        print("raw_text:", raw_text)
        print("this is docx file")
        print(file.filename)

    print("end: parse text")

    """
    import subprocess
    from os import getcwd
    result = subprocess.run(["npx", "textlint", "--format", "json", "--stdin"],
                            cwd=getcwd()+"/textlint", input=raw_text, encoding='utf-8', stdout=subprocess.PIPE)
    # print("end: textlint")
    """

    import requests
    import os
    api_scheme = os.getenv("TEXTLINT_API_SCHEME", "http")
    api_addr = os.getenv("TEXTLINT_API_ADDR", "backend")
    api_port = int(os.getenv("TEXTLINT_API_PORT", 3000))
    res = requests.post(
        f"{api_scheme}://{api_addr}:{api_port}/textlint",
        data=raw_text.encode('utf-8')
    )
    fix_res = []
    print("target:", api_addr, api_port)
    print("status-code:", res.status_code)
    print("req-url", res.url)
    print("response:", res.json())
    print("end: textlint")
    for i in res.json():
        cutting_text = raw_text[i['index']-4:i['index']+5]
        i['cutting_text'] = cutting_text
        fix_res.append(
            {'index': i['index']+1, 'cutting_text': cutting_text, 'message': i['message']})
    print(fix_res)
    return {"result": fix_res}
    # return {"result": res.json()}

    """
    import json
    result_json = json.loads(result.stdout)
    return {"result": result_json[0]["messages"]}
    """
