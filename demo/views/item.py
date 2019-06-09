import sqlalchemy as sa
import json
from demo.models import Invoice, InvoiceItem
from pyramid.view import view_config
from demo.views.utils import validateIntegers, validateFloats, success, failure

    
@view_config(route_name='item', match_param='action=create', renderer='json', request_method='POST')
def item_create(request):
    requestJSON = request.json_body

    for arg in ['units', 'description', 'amount', 'parent_id']:
        if not requestJSON.get(arg):
            return failure('expected '+ arg + ' to be supplied.')
    
    error = validateIntegers(requestJSON, ['units', 'parent_id'])
    if error:
        return error

    error = validateFloats(requestJSON, ['amount'])
    if error:
        return error
    
    entry = InvoiceItem(
        units = int(requestJSON['units']),
        description = requestJSON['description'],
        amount = float(requestJSON['amount']),
        parent_id = int(requestJSON['parent_id']))

    request.dbsession.add(entry)
    request.dbsession.flush()
    query = request.dbsession.query(InvoiceItem)
    item = query.get(entry.id)
    return success(payload=json.dumps(item.to_json()))
