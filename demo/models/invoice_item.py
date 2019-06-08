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

    def to_json(self):
        to_serialize = ['id', 'units', 'description', 'amount', 'parent_id']
        d = {}
        for attr_name in to_serialize:
            d[attr_name] = getattr(self, attr_name)
        d['amount'] = float(d['amount'])            
        return d
