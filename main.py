from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse , RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.staticfiles import StaticFiles
from os import system
from time import sleep
from re import match
from random import choice , randrange
from tinydb import TinyDB,Query


dbase = TinyDB('db.json')
db = {}
app = FastAPI()
q = Query()

templates = Jinja2Templates(directory="temp")
app.mount("/html/static", StaticFiles(directory="temp/html/"), name="html_static")
        
def read(filename):
 with open(filename , "r", encoding="utf-8") as f:
   return f.read()

def randemoji():
    s = str()
    a = list(read("emoji.txt").split())
    for i in range(int(randrange(1,5))):
        s += choice(a)
    return s
    
def add_to_database(url):
    emoji = randemoji()
    u = dbase.search(q.link == url)
    e = dbase.search(q.emo == emoji)
    if not u:
        if not e:
            dbase.insert({'link':url,'emo':emoji})
  

@app.get('/')
def generate(request: Request,url="nvn"):
    url = url.lower()
    pedaret = request.base_url
    if url == "nvn":
        return templates.TemplateResponse("html/home.html", {"request":request})
    else:
        url = url if match("^https://|^http://", url) else "https://" + url
        m = dbase.search(q.link == url)
        if m:
            url_jadid = str(pedaret)+str(m[0]['emo'])
            return templates.TemplateResponse("html/home.html", {"request":request,"new_url":url_jadid})
        else:
            add_to_database(url=url)
            m = dbase.search(q.link == url)
            if m:
                url_jadid = str(pedaret)+str(m[0]['emo'])
                return templates.TemplateResponse("html/home.html", {"request":request,"new_url":url_jadid})


@app.get('/{id}')
def redirect(id,request:Request):
    m = dbase.search(q.emo == id)
    if m:
        try:
            return templates.TemplateResponse("html/wait.html", {"request":request,"redirect_url":m[0]['link']})
        except:
            return templates.TemplateResponse("html/404.html", {"request":request})
