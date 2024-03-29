from fastapi import FastAPI, Request, Depends, Form, UploadFile, File, Query
from typing import Optional
from fastapi.responses import Response
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from viewmodels.metadata.metadata_view_model import PageMetadataViewModel
from viewmodels.accounts.accounts_view_model import AccountsViewModel
from viewmodels.settings.settings_view_model import SettingsViewModel
from viewmodels.transaction_history.transaction_history_view_model import TransactionHistoryViewModel
import json
import os

import app.sqlite_database as db
import app.csv_loader.conversion_blueprint as conversion_blueprint
import app.csv_loader.csv_file_manger as csv_file_manger
import app.flowchart as flowchart
import app.csv_loader.csv_convert as csv_convert
import app.transaction_history.aggregate as aggregate
import app.llm_enhancer.bank_gpt as b_gpt
import app.llm_enhancer.enhancer as enhancer


app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")
db.startup_event()
csv_file_manger.check_and_create_file_dir()


try:
    with open("./data/app_data.json", "r") as data_file:
        app_data = json.load(data_file)
except IOError:
    print("Error loading app_data.json")
    app_data = {}

pages = [
    {"title": "Dashboard", "route": "/", "template": "pages/dashboard.html"},
    {"title": "Transactions History", "route": "/transactions", "template": "pages/transaction_history/transaction_history.html", "viewModel": TransactionHistoryViewModel},
    {"title": "Bank Accounts", "route": "/banks", "template": "pages/banks/banks.html", "viewModel": AccountsViewModel},
    {"title": "Settings", "route": "/settings", "template": "pages/settings/settings.html", "viewModel": SettingsViewModel},
]

async def page_metadata(request: Request) -> PageMetadataViewModel:
    return PageMetadataViewModel(request, app_data.get('metadata'))


def find_page(page_name: str):
    return next((page for page in pages if page["route"].strip("/") == page_name), None)

@app.get("/accounts")
async def get_accounts(request: Request):
    return AccountsViewModel(request).get_accounts()

@app.post("/new_account")
async def new_account(request: Request):
    name = "New Account"
    account_number = None
    db_id = AccountsViewModel(request).add_account(name, account_number)
    csv_file_manger.create_sub_folder_bank_account(db_id)
    if request.headers.get('HX-Request') == 'true':
        return templates.TemplateResponse("pages/banks/partials/account_list_element.html", {"request": request, "account": {"name": name, "id": db_id}})
    else:
        return {"status": "success", "id": db_id, "name": name}

@app.patch("/update_account/{id}")
async def update_account(request: Request, id: int, name: str = Form(...), account_number: Optional[str] = Form(None), csv_seperator: str = Form(None), csv_columns: str = Form(None), csv_file: Optional[UploadFile] = File(None), flowchart_diagram: str = Form(None)):
    print("update_account" + str(id) + " " + name)
    csv_file_name = None
    if csv_file:
        csv_file_name = csv_file.filename
    if AccountsViewModel(request).update_account(id, name, account_number, csv_seperator, csv_columns, csv_file_name=csv_file_name, flowchart_diagram=flowchart_diagram):
        if csv_file:
            await csv_file_manger.save_csv_file(csv_file, id)
        if request.headers.get('HX-Request') == 'true':
            return templates.TemplateResponse("pages/banks/partials/account_list_element.html",
                                              {"request": request, "account": {"name": name, "id": id}})
            return Response(content='', status_code=200)
        else:
            return {"status": "success"}

@app.post("/apply_flowchart/{id}")
async def apply_flowchart(request: Request, id: int):
    flowchart_diagram = AccountsViewModel(request).get_account(id)["flowchart_diagram"]
    if flowchart_diagram:
        function_chain = flowchart.build_conversion_functions(flowchart_diagram)
        converted = csv_convert.convert_csv(f"csv_files/{id}/transactions.csv", ";", function_chain)
        await csv_file_manger.save_dict_to_csv_file(converted, id, "converted")
        return {"status": "success"}


@app.post("/generate_transaction_history")
async def generate_transaction_history(request: Request):
    accounts = []
    for account in AccountsViewModel(request).get_accounts():
        # check if account csv dir has file converted.csv
        if os.path.exists(f"csv_files/{account['id']}/converted.csv"):
            pandas = await csv_file_manger.load_converted_csv_to_pandas(account["id"])
            # add column for account_id
            pandas["account_id"] = account["id"]
            accounts.append(pandas)
    aggregated = aggregate.combine_and_filter_bank_accounts(accounts)
    bank_gpt = b_gpt.ChatGPTBanking(api_key=db.get_settings()["api_key"], model=db.get_settings()["gpt_api_model"])
    enhanced = enhancer.extracting_process(bank_gpt, aggregated, 3)
    print("enhanced data")
    await csv_file_manger.save_pandas_to_csv(enhanced, "transaction_history", "enhanced")
    print("saved enhanced data")
    #enhanced = await csv_file_manger.load_transactions_csv_to_pandas()
    TransactionHistoryViewModel(request).upsert_transaction_pd_df(enhanced)

    #vector_db.load_dataframe(enhanced)


@app.get("/transactions-history")
async def transactions(request: Request, search: Optional[str] = Query(None), date_range_min: Optional[str] = Query(None), date_range_max: Optional[str] = Query(None)):
    print("transactions")
    print(search)
    print(date_range_min)
    print(date_range_max)
    transactions_history = TransactionHistoryViewModel(request).search_transaction_history(search, date_range_min, date_range_max)
    return templates.TemplateResponse("pages/transaction_history/partials/table_body.html", {"request": request, "transaction_history": transactions_history })



@app.put("/settings")
async def update_settings(request: Request, currency: str = Form(...), api_key: str = Form(...), gpt_api_model: str = Form(...)):
    settings = SettingsViewModel(request).upsert_settings(currency, api_key, gpt_api_model)
    if request.headers.get('HX-Request') == 'true':
        return templates.TemplateResponse("pages/settings/partials/settings_form.html", {"request": request, "settings": settings})
    return {"status": "success"}


@app.get("/account_settings/{id}")
async def account_settings(request: Request, id: int):
    print("account_settings")
    account = AccountsViewModel(request).get_account(id)
    draggable_elements = [element.to_js_dict() for element in flowchart.draggable_elements]
    return templates.TemplateResponse("pages/banks/partials/account_settings_form.html", {"request": request, "account": account, "draggable_elements": draggable_elements,"conversion_format": json.dumps(conversion_blueprint.data_columns)})

@app.delete("/delete_account/{id}")
async def delete_account(request: Request, id: int):
    if AccountsViewModel(request).delete_account(id):
        csv_file_manger.delete_sub_folder_bank_account(id)
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
