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
    print("end: parse text")

    import subprocess
    from os import getcwd
    result = subprocess.run(["npx", "textlint", "--format", "json", "--stdin"], \
        cwd=getcwd()+"/textlint", input=raw_text, encoding='utf-8', stdout=subprocess.PIPE)
    print("end: textlint")

    import json
    result_json = json.loads(result.stdout)
    return {"result": result_json[0]["messages"]}