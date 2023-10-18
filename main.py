import uvicorn
from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse
from starlette.staticfiles import StaticFiles

app = FastAPI()

app.mount("/", StaticFiles(directory="chatsite",html = True), name="chatsite")
@app.get("/", response_class=HTMLResponse)
async def read_html_file(request: Request):
    with open("chatsite/index.html", "r") as file:
        html_content = file.read()
        print(html_content)
    return html_content

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=27358)