from fastapi import FastAPI
from fastapi import Request
from fastapi import File
from fastapi import UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def top(request: Request):
    return templates.TemplateResponse("top.html", {"request": request})


@app.post("/api/v1/analysis")
async def upload(file: UploadFile = File(...)):
    import pdf_to_text
    raw_text = pdf_to_text.pdf_to_text(file.file)
    print("raw_text:", raw_text)
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
    api_addr = os.getenv("TEXTLINT_API_ADDR", "backend")
    api_port = int(os.getenv("TEXTLINT_API_PORT", 3000))
    res = requests.post(
        f"http://{api_addr}:{api_port}/textlint",
        data=raw_text.encode('utf-8')
    )
    print("target:", api_addr, api_port)
    print("response:", res.json())
    print("end: textlint")
    return {"result": res.json()}

    """
    import json
    result_json = json.loads(result.stdout)
    return {"result": result_json[0]["messages"]}
    """
