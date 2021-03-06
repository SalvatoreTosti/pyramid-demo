import json

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

def validateJSON(request):
    try:
        request.json_body
    except json.decoder.JSONDecodeError:
        return failure('malformed JSON message.')

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

def validatePositiveIntegers(dictionary, values):
    for arg in values:
        value = dictionary.get(arg)
        integer = int(value)
        if integer < 0:
            return failure('expected '+ arg + ' to be a positive integer value.')

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

def validatePositiveFloats(dictionary, values):
    for arg in values:
        value = dictionary.get(arg)
        flt = float(value)
        if flt < 0:
            return failure('expected '+ arg + ' to be a positive float value.')
 
    