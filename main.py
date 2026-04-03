from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import json
import os
from datetime import datetime
from collections import defaultdict

app = FastAPI()
templates = Jinja2Templates(directory="templates")

FILE = "data.json"

# Load data
def load_data():
    if not os.path.exists(FILE):
        return []
    try:
        with open(FILE, "r") as f:
            return json.load(f)
    except:
        return []

# Save data
def save_data(data):
    with open(FILE, "w") as f:
        json.dump(data, f)

# Suggestions
def get_suggestions(expenses):
    total = sum(e["amount"] for e in expenses)
    suggestions = []

    if total > 15000:
        suggestions.append("Reduce unnecessary expenses")
    if any(e["category"] == "milk" and e["amount"] > 2000 for e in expenses):
        suggestions.append("Check milk expenses")
    if any(e["category"] == "gas" for e in expenses):
        suggestions.append("Use fuel efficiently")
    if any(e["category"] == "current" for e in expenses):
        suggestions.append("Reduce electricity usage")
    if any(e["category"] == "food" and e["amount"] > 3000 for e in expenses):
        suggestions.append("Control outside food spending")

    if not suggestions:
        suggestions.append("Spending looks balanced")

    return suggestions

# Home page
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    expenses = load_data()
    total = sum(e["amount"] for e in expenses)

    category_data = defaultdict(float)
    for e in expenses:
        category_data[e["category"]] += e["amount"]

    categories = list(category_data.keys())
    amounts = list(category_data.values())

    suggestions = get_suggestions(expenses)

    return templates.TemplateResponse("index.html", {
        "request": request,
        "expenses": expenses,
        "total": total,
        "categories": categories,
        "amounts": amounts,
        "suggestions": suggestions
    })

# Add expense
@app.post("/add")
def add(
    name: str = Form(...),
    amount: float = Form(...),
    category: str = Form(...)
):
    data = load_data()

    data.append({
        "name": name,
        "amount": amount,
        "category": category,
        "date": datetime.now().strftime("%Y-%m-%d")
    })

    save_data(data)

    return RedirectResponse("/", status_code=303)