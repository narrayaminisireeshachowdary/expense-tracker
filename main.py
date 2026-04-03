from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import sqlite3
from datetime import datetime

app = FastAPI()

templates = Jinja2Templates(directory="templates")

# Database connection
conn = sqlite3.connect("expenses.db", check_same_thread=False)
cursor = conn.cursor()

# Create table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    amount REAL,
    category TEXT,
    date TEXT
)
""")
conn.commit()


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    cursor.execute("SELECT title, amount, category, date FROM expenses")
    rows = cursor.fetchall()

    expenses = []
    total = 0

    for r in rows:
        expenses.append({
            "title": r[0],
            "amount": r[1],
            "category": r[2],
            "date": r[3]
        })
        total += r[1]

    return templates.TemplateResponse("index.html", {
        "request": request,
        "expenses": expenses,
        "total": total
    })


@app.post("/add")
async def add_expense(
    title: str = Form(...),
    amount: float = Form(...),
    category: str = Form(...)
):
    date = datetime.now().strftime("%Y-%m-%d")

    cursor.execute(
        "INSERT INTO expenses (title, amount, category, date) VALUES (?, ?, ?, ?)",
        (title, amount, category, date)
    )
    conn.commit()

    return RedirectResponse(url="/", status_code=303)