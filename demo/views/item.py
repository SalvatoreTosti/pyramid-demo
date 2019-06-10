import sqlalchemy as sa
import json
from demo.models import Invoice, InvoiceItem
from pyramid.view import view_config
from demo.views.utils import validateJSON, validateIntegers, validatePositiveIntegers, validateFloats, validatePositiveFloats, success, failure
    
@view_config(route_name='item', match_param='action=create', renderer='json', request_method='POST')
def item_create(request):
    error = validateJSON(request)
    if error:
        return error
        
    requestJSON = request.json_body

    for arg in ['units', 'description', 'amount', 'parent_id']:
        if not requestJSON.get(arg):
            return failure('expected '+ arg + ' to be supplied.')
    
    error = validateIntegers(requestJSON, ['units', 'parent_id'])
    if error:
        return error
        
    error = validatePositiveIntegers(requestJSON, ['units', 'parent_id'])
    if error:
        return error

    error = validateFloats(requestJSON, ['amount'])
    if error:
        return error
    
    error = validatePositiveFloats(requestJSON, ['amount'])
    if error:
        return error
    
    parentID = int(requestJSON['parent_id'])    
    if not request.dbsession.query(Invoice).get(parentID):
        return failure("specified parent ID does not exist.")
    
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
