import sqlalchemy as sa
import json
from demo.models import Invoice, InvoiceItem
from pyramid.view import view_config
    
@view_config(route_name='item', match_param='action=create', renderer='json')
def item_create(request):
    requestJSON = request.json_body
    entry = InvoiceItem(
        units = requestJSON['units'],
        description = requestJSON['description'],
        amount = requestJSON['amount'],
        parent_id = requestJSON['parent_id'])

    request.dbsession.add(entry)
    request.dbsession.flush()
    query = request.dbsession.query(InvoiceItem)
    item = query.get(entry.id)
    return item.to_json()
