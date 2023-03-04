from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.staticfiles import StaticFiles
from random import choice, randrange
from tinydb import TinyDB, Query

# define app
app = FastAPI()

# define global variables
db = TinyDB('db.json')
q = Query()
templates = Jinja2Templates(directory="temp")
app.mount("/html/static", StaticFiles(directory="temp/html/"), name="html_static")

# define helper functions
def read(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return f.read()

def randemoji():
    a = list(read("emoji.txt").split())
    return ''.join([choice(a) for _ in range(randrange(1, 5))])

def add_to_database(url):
    emoji = randemoji()
    if not db.contains(q.link == url) and not db.contains(q.emo == emoji):
        db.insert({'link': url, 'emo': emoji})

# define endpoints
@app.get('/')
def generate(request: Request, url: str = "nvn"):
    url = url.lower()
    if url == "nvn":
        return templates.TemplateResponse("html/home.html", {"request": request})
    else:
        url = url if match("^https://|^http://", url) else "https://" + url
        m = db.search(q.link == url)
        if m:
            new_url = str(request.base_url) + str(m[0]['emo'])
            return templates.TemplateResponse("html/home.html", {"request": request, "new_url": new_url})
        else:
            add_to_database(url)
            m = db.search(q.link == url)
            if m:
                new_url = str(request.base_url) + str(m[0]['emo'])
                return templates.TemplateResponse("html/home.html", {"request": request, "new_url": new_url})

@app.get('/{id}')
def redirect(id: str, request: Request):
    m = db.search(q.emo == id)
    if m:
        try:
            return templates.TemplateResponse("html/wait.html", {"request": request, "redirect_url": m[0]['link']})
        except:
            return templates.TemplateResponse("html/404.html", {"request": request})
