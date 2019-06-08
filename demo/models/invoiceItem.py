import datetime
from sqlalchemy import (
    Column,
    Integer,
    Text,
    DateTime,
    NUMERIC
)

from .meta import Base

class InvoiceItem(Base):
    __tablename__ = 'invoice_items'
    id = Column(Integer, primary_key=True)
    units = Column(Integer)
    description = Column(Text)
    amount = Column(NUMERIC)
    invoice = relationship("Invoice", back_populates="items")
    