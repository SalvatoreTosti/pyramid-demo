def failure(message, status=400):
    return {
        'status' : status,
        'message' : message,
        'payload' : ''
    }

def success(message='success.', payload='', status=200):
    return {
        'status' : status,
        'message': message,
        'payload' : payload
    }

def _validateInteger(value, valueName):
    try:
        int(value)
    except (ValueError, TypeError):
        return failure('expected '+ valueName + ' to be an integer value.')
        
def validateIntegers(dictionary, values):
    for arg in values:
        errorMessage = _validateInteger(dictionary.get(arg), arg)
        if errorMessage:
            return errorMessage

def _validateFloat(value, valueName):
    try:
        float(value)
    except ValueError:
        return failure('expected '+ valueName + ' to be a float value.')   

def validateFloats(dictionary, values):
    for arg in values:
        errorMessage = _validateFloat(dictionary.get(arg), arg)
        if errorMessage:
            return errorMessage  
    