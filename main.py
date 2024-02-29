from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import json

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

try:
    with open("data/app_data.json", "r") as data_file:
        app_data = json.load(data_file)
except IOError:
    print("Error loading app_data.json")
    app_data = {}

pages = [
    {"title": "Dashboard", "route": "/", "template": "pages/dashboard.html"},
    {"title": "Transactions History", "route": "/transactions", "template": "pages/transaction_history.html"},
    {"title": "Bank Accounts", "route": "/banks", "template": "pages/banks.html"},
    {"title": "Settings", "route": "/settings", "template": "pages/settings.html"},
]

async def page_metadata() -> dict:
    return app_data.get('metadata', {})

async def handle_request(request: Request, template_name: str, context: dict):
    if request.headers.get('HX-Request') == 'true':
        return templates.TemplateResponse(template_name, context)
    else:
        context["main_content_template"] = template_name
        return templates.TemplateResponse("base.html", context)



@app.get("/{page_name:path}")
async def page_handler(request: Request, page_name: str = "", metadata: dict = Depends(page_metadata)):
    context = {"request": request, "metadata": metadata, "pages": pages}
    page = next((page for page in pages if page["route"].strip("/") == page_name), None)

    if page:
        return await handle_request(request, page["template"], context)
    else:
        return await handle_request(request, "pages/404.html", context)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
