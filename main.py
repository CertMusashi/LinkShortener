from fastapi import FastAPI
from fastapi.responses import HTMLResponse 
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.staticfiles import StaticFiles
from os import system
from re import match
from random import choice , randrange



db = {}
app = FastAPI()

templates = Jinja2Templates(directory="temp")
app.mount("/html/css", StaticFiles(directory="temp/html/css"), name="html_static")


def write(name,txt):
    with open(name,"w",encoding="utf-8") as f:
        f.write(txt)
        f.close()
        
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
    if url not in db.keys():
        if emoji not in db.values():
            db[url] = emoji
  

@app.get('/')
def generate(request: Request,url="nvn"):
    pedaret = request.base_url
    if url == "nvn" or url == "":
        url_jadid = "محل قرار گیری لینک جدید"
        return templates.TemplateResponse("html/home.html", {"request":request ,"new_url":"","view":url_jadid})
    else:
        url = url if match("^https://|^http://", url) else "https://" + url
        if url in db.keys():
            url_jadid = str(pedaret)+str(db[url])
            return templates.TemplateResponse("html/home.html", {"request":request,"new_url":url_jadid,"view":url_jadid})
        else:
            add_to_database(url=url)
            url_jadid = str(pedaret)+str(db[url])
            return templates.TemplateResponse("html/home.html", {"request":request,"new_url":url_jadid,"view":url_jadid})

  
@app.get('/{id}')
def redirect(id,request:Request):
    key_list = list(db.keys())
    value_list = list(db.values())
    try:
        x = value_list.index(id)
        if type(x) == int:
            return templates.TemplateResponse("html/wait.html", {"request":request,"redirect_url":key_list[x]})
    except:
        return templates.TemplateResponse("html/404.html", {"request":request})
    
    
if __name__ == "__main__":
    system("uvicorn main:app")