import datetime
from sqlalchemy import (
    Column,
    Integer,
    DateTime,
)

from .meta import Base

class Invoice(Base):
    __tablename__ = 'invoices'
    id = Column(Integer, primary_key=True)
    date = Column(DateTime, default=datetime.datetime.utcnow)
    items = relationship("InvoiceItem", back_populates="invoice")
