from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="templates")

expenses = []


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    total = sum(e["amount"] for e in expenses)

    return templates.TemplateResponse("index.html", {
        "request": request,
        "expenses": expenses,
        "total": total
    })


@app.post("/add")
async def add_expense(
    title: str = Form(...),
    amount: float = Form(...)
):
    expenses.append({
        "title": title,
        "amount": amount
    })

    return RedirectResponse("/", status_code=303)