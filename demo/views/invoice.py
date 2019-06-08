import sqlalchemy as sa
import json
from demo.models import Invoice, InvoiceItem
from pyramid.view import view_config

@view_config(route_name='invoice', match_param='action=view', renderer='json')
def invoice_view(request):
    query = request.dbsession.query(Invoice)
    invoices = query.order_by(sa.desc(Invoice.date)).all()
    payload = {}
    for invoice in invoices:
        payload[invoice.id] = {
            'invoice' : invoice.to_json(),
            'items' : []}
    
    query = request.dbsession.query(InvoiceItem)
    invoiceItems = query.order_by(sa.desc(InvoiceItem.id)).all()
    
    for item in invoiceItems:
        parentID = item.parent_id
        payload[parentID]['items'].append(item.to_json())
    return {'invoices': payload}
    
@view_config(route_name='invoice', match_param='action=create', renderer='json')
def invoice_create(request):
    entry = Invoice()
    request.dbsession.add(entry)
    request.dbsession.flush()
    invoice = request.dbsession.query(Invoice).get(entry.id)
    return invoice.to_json()
