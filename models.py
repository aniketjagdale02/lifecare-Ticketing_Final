from sqlalchemy import Column, Integer, String
from database import Base

class Ticket(Base):
    __tablename__ = "tickets"
    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(String, unique=True, index=True)
    customer_name = Column(String)
    email_id = Column(String)
    contact_name = Column(String)
    title = Column(String)
    description = Column(String)
    status = Column(String)
    assigned_to = Column(String)
    priority = Column(String)
    category = Column(String)
