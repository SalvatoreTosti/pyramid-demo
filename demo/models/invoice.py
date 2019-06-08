import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column,
    Integer,
    DateTime
)

from .meta import Base

class Invoice(Base):
    __tablename__ = 'invoices'
    id = Column(Integer, primary_key=True)
    date = Column(DateTime, default=datetime.datetime.utcnow)
    # children = relationship("InvoiceItem", backref="invoices")

    def to_json(self):
        to_serialize = ['id', 'date']
        d = {}
        for attr_name in to_serialize:
            d[attr_name] = getattr(self, attr_name)
        d['date'] = d['date'].isoformat()
        return d
