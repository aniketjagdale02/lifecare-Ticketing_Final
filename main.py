from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from sqlalchemy import asc
import uuid

from database import SessionLocal, engine
import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_tickets(request: Request, db: Session = Depends(get_db)):
    tickets = db.query(models.Ticket).order_by(asc(models.Ticket.id)).all()
    return templates.TemplateResponse("dashboard.html", {"request": request, "tickets": tickets})

@app.get("/create")
def create_ticket_form(request: Request):
    return templates.TemplateResponse("create.html", {"request": request})

@app.post("/create")
def create_ticket(
    request: Request,
    customer_name: str = Form(...),
    email_id: str = Form(...),
    contact_name: str = Form(...),
    title: str = Form(...),
    description: str = Form(...),
    status: str = Form(...),
    assigned_to: str = Form(...),
    priority: str = Form(...),
    category: str = Form(...),
    db: Session = Depends(get_db)
):
    ticket_id = str(uuid.uuid4())[:8]
    new_ticket = models.Ticket(
        ticket_id=ticket_id,
        customer_name=customer_name,
        email_id=email_id,
        contact_name=contact_name,
        title=title,
        description=description,
        status=status,
        assigned_to=assigned_to,
        priority=priority,
        category=category
    )
    db.add(new_ticket)
    db.commit()
    return RedirectResponse(url="/", status_code=303)

@app.get("/edit/{ticket_id}")
def edit_ticket_form(ticket_id: int, request: Request, db: Session = Depends(get_db)):
    ticket = db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return templates.TemplateResponse("edit.html", {"request": request, "ticket": ticket})

@app.post("/edit/{ticket_id}")
def edit_ticket(ticket_id: int,
    request: Request,
    customer_name: str = Form(...),
    email_id: str = Form(...),
    contact_name: str = Form(...),
    title: str = Form(...),
    description: str = Form(...),
    status: str = Form(...),
    assigned_to: str = Form(...),
    priority: str = Form(...),
    category: str = Form(...),
    db: Session = Depends(get_db)
):
    ticket = db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    ticket.customer_name = customer_name
    ticket.email_id = email_id
    ticket.contact_name = contact_name
    ticket.title = title
    ticket.description = description
    ticket.status = status
    ticket.assigned_to = assigned_to
    ticket.priority = priority
    ticket.category = category

    db.commit()
    return RedirectResponse(url="/", status_code=303)
