import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column,
    Integer,
    Text,
    DateTime,
    NUMERIC,
    ForeignKey
)

from .meta import Base

class InvoiceItem(Base):
    __tablename__ = 'invoice_items'
    id = Column(Integer, primary_key=True)
    units = Column(Integer)
    description = Column(Text)
    amount = Column(NUMERIC)
    parent_id = Column(Integer, ForeignKey('invoices.id'))
    # invoice = relationship("Invoice", back_populates="items")
    
