from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import Response, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from viewmodels.metadata.metadata_view_model import PageMetadataViewModel
from viewmodels.accounts.accounts_view_model import AccountsViewModel
from pydantic import BaseModel
import json
import app.database as db

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")
db.startup_event()

try:
    with open("./data/app_data.json", "r") as data_file:
        app_data = json.load(data_file)
except IOError:
    print("Error loading app_data.json")
    app_data = {}

pages = [
    {"title": "Dashboard", "route": "/", "template": "pages/dashboard.html"},
    {"title": "Transactions History", "route": "/transactions", "template": "pages/transaction_history.html"},
    {"title": "Bank Accounts", "route": "/banks", "template": "pages/banks/banks.html", "viewModel": AccountsViewModel},
    {"title": "Settings", "route": "/settings", "template": "pages/settings.html"},
]

async def page_metadata(request: Request) -> PageMetadataViewModel:
    return PageMetadataViewModel(request, app_data.get('metadata'))


def find_page(page_name: str):
    return next((page for page in pages if page["route"].strip("/") == page_name), None)

@app.get("/accounts")
async def get_accounts(request: Request):
    return AccountsViewModel(request).accounts

@app.post("/new_account")
async def new_account(request: Request):
    name = "New Account"
    account_number = None
    db_id = AccountsViewModel(request).add_account(name, account_number)
    if request.headers.get('HX-Request') == 'true':
        return templates.TemplateResponse("pages/banks/partials/account_list_element.html", {"request": request, "account": {"name": name, "id": db_id}})
    else:
        return {"status": "success", "id": db_id, "name": name}
@app.delete("/delete_account/{id}")
async def delete_account(request: Request, id: int):
    if AccountsViewModel(request).delete_account(id):
        if request.headers.get('HX-Request') == 'true':
            return Response(content='', status_code=200)
        else:
            return {"status": "success"}

@app.get("/{page_name:path}")
async def page_handler(request: Request, page_name: str = "", metadata: PageMetadataViewModel = Depends(page_metadata)):
    context = {"request": request, "metadata": metadata.to_dict(), "pages": pages}
    page = find_page(page_name)

    template_name = page["template"] if page else "pages/404.html"

    if page and "viewModel" in page:
        viewmodel_instance = page["viewModel"](request)
        context["page_data"] = viewmodel_instance.to_dict()

    if request.headers.get('HX-Request') == 'true':
        return templates.TemplateResponse(template_name, context)
    else:
        context["main_content_template"] = template_name
        return templates.TemplateResponse("base.html", context)






if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
