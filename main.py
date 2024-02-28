from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from viewmodels.metadata.metadata_view_model import PageMetadataViewModel

import json


app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

with open("data/app_data.json", "r") as data_file:
    app_data = json.load(data_file)



@app.get("/")
async def root(request: Request):
    app_data.get('metadata')
    vm = PageMetadataViewModel(request, app_data.get('metadata'))
    return templates.TemplateResponse("base.html", {"request": request, "page": vm.to_dict()})
