from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import sqlite3
import uuid

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

def init_db():
    conn = sqlite3.connect("tickets.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tickets (
        id TEXT PRIMARY KEY,
        customer_name TEXT,
        email TEXT,
        contact TEXT,
        issue_title TEXT,
        description TEXT,
        status TEXT,
        assigned_to TEXT,
        priority TEXT,
        category TEXT
    )''')
    conn.commit()
    conn.close()

init_db()

@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    conn = sqlite3.connect("tickets.db")
    c = conn.cursor()
    c.execute("SELECT * FROM tickets")
    tickets = c.fetchall()
    conn.close()
    return templates.TemplateResponse("dashboard.html", {"request": request, "tickets": tickets})

@app.get("/create", response_class=HTMLResponse)
def create_ticket_form(request: Request):
    return templates.TemplateResponse("create_ticket.html", {"request": request})

@app.post("/create")
def create_ticket(
    customer_name: str = Form(...),
    email: str = Form(...),
    contact: str = Form(...),
    issue_title: str = Form(...),
    description: str = Form(...),
    status: str = Form(...),
    assigned_to: str = Form(...),
    priority: str = Form(...),
    category: str = Form(...)
):
    ticket_id = str(uuid.uuid4())[:8]
    conn = sqlite3.connect("tickets.db")
    c = conn.cursor()
    c.execute("INSERT INTO tickets VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
              (ticket_id, customer_name, email, contact, issue_title, description, status, assigned_to, priority, category))
    conn.commit()
    conn.close()
    return RedirectResponse("/", status_code=302)

@app.get("/edit/{ticket_id}", response_class=HTMLResponse)
def edit_ticket_form(request: Request, ticket_id: str):
    conn = sqlite3.connect("tickets.db")
    c = conn.cursor()
    c.execute("SELECT * FROM tickets WHERE id = ?", (ticket_id,))
    ticket = c.fetchone()
    conn.close()
    if not ticket:
        return HTMLResponse("Ticket not found", status_code=404)
    return templates.TemplateResponse("edit_ticket.html", {"request": request, "ticket": ticket})

@app.post("/edit/{ticket_id}")
def update_ticket(
    ticket_id: str,
    customer_name: str = Form(...),
    email: str = Form(...),
    contact: str = Form(...),
    issue_title: str = Form(...),
    description: str = Form(...),
    status: str = Form(...),
    assigned_to: str = Form(...),
    priority: str = Form(...),
    category: str = Form(...)
):
    conn = sqlite3.connect("tickets.db")
    c = conn.cursor()
    c.execute('''UPDATE tickets SET
        customer_name=?, email=?, contact=?, issue_title=?,
        description=?, status=?, assigned_to=?, priority=?, category=?
        WHERE id=?''',
        (customer_name, email, contact, issue_title, description, status, assigned_to, priority, category, ticket_id))
    conn.commit()
    conn.close()
    return RedirectResponse("/", status_code=302)

@app.get("/delete/{ticket_id}")
def delete_ticket(ticket_id: str):
    conn = sqlite3.connect("tickets.db")
    c = conn.cursor()
    c.execute("DELETE FROM tickets WHERE id = ?", (ticket_id,))
    conn.commit()
    conn.close()
    return RedirectResponse("/", status_code=302)
