from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Templates folder
templates = Jinja2Templates(directory="templates")

# Static files (optional but recommended)
app.mount("/static", StaticFiles(directory="static"), name="static")


# Sample data (IMPORTANT: keep it simple list of dicts)
expenses = []


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "expenses": expenses
    })


@app.post("/add")
async def add_expense(
    request: Request,
    title: str = Form(...),
    amount: float = Form(...)
):
    # Append as dict (safe format)
    expenses.append({
        "title": title,
        "amount": amount
    })

    return templates.TemplateResponse("index.html", {
        "request": request,
        "expenses": expenses
    })