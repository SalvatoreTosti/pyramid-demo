import sqlalchemy as sa
import json
import datetime
from demo.models import Invoice, InvoiceItem
from pyramid.view import view_config
from demo.views.utils import validateJSON, validateIntegers, success


@view_config(route_name='invoices',
             renderer='demo:templates/invoice.jinja2')
def invoice_html(request):
    return {}

@view_config(route_name='invoice', match_param='action=view', renderer='json', request_method='POST')
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
    return success(payload=json.dumps({ 'invoices' : payload }))
    
@view_config(route_name='invoice', match_param='action=create', renderer='json', request_method='POST')
def invoice_create(request):
    try:
        requestJSON =request.json_body
    except json.decoder.JSONDecodeError:
        requestJSON = {}
        
    if 'date' in requestJSON:
        error = validateIntegers(requestJSON, ['date'])
        if error:
            return error
            
        seconds = int(requestJSON['date'])
        date = datetime.datetime.fromtimestamp(seconds) #assumes date comes through as seconds since epoch, UTC
        entry = Invoice(date=date)
    else:
        entry = Invoice()
    
    request.dbsession.add(entry)
    request.dbsession.flush()
    invoice = request.dbsession.query(Invoice).get(entry.id) 
    return success(payload=json.dumps(invoice.to_json()))
