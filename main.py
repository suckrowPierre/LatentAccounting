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

pages = [
    {
        "title": "Dashboard",
        "route": "/"
    },
    {
        "title": "Transactions History",
        "route": "/transactions"
    },
    {
        "title": "Bank Accounts",
        "route": "/banks"
    },
    {
        "title": "Settings",
        "route": "/settings"
    }
]


async def get_full_html(request, route):
    page_templates = {
        "/": "pages/dashboard.html",
        "/transactions": "pages/transaction_history.html",
        "/banks": "pages/banks.html",
        "/settings": "pages/settings.html",
    }
    selected_template = page_templates.get(route, "pages/404.html")

    app_data.get('metadata')
    vm = PageMetadataViewModel(request, app_data.get('metadata'))

    return templates.TemplateResponse("base.html", {"request": request, "page": vm.to_dict(), "pages": pages,
                                                    "main_content_template": selected_template})


@app.get("/")
async def root(request: Request):
    if request.headers.get('HX-Request') == 'true':
        print("htmx")
        return templates.TemplateResponse("pages/dashboard.html", {"request": request})
    return await get_full_html(request, "/")


@app.get("/transactions")
async def transactions(request: Request):
    if request.headers.get('HX-Request') == 'true':
        print("htmx")
        return templates.TemplateResponse("pages/transaction_history.html", {"request": request})
    return await get_full_html(request, "/transactions")

@app.get("/banks")
async def banks(request: Request):
    if request.headers.get('HX-Request') == 'true':
        print("htmx")
        return templates.TemplateResponse("pages/banks.html", {"request": request})
    return await get_full_html(request, "/banks")

@app.get("/settings")
async def settings(request: Request):
    if request.headers.get('HX-Request') == 'true':
        print("htmx")
        return templates.TemplateResponse("pages/settings.html", {"request": request})
    return await get_full_html(request, "/settings")


