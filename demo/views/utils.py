def _validateInteger(value, valueName):
    try:
        int(value)
    except (ValueError, TypeError):
        return {
            'status' : '400',
            'message' : 'expected '+ valueName + ' to be an integer value.'
        }
        
def validateIntegers(dictionary, values):
    for arg in values:
        errorMessage = _validateInteger(dictionary.get(arg), arg)
        if errorMessage:
            return errorMessage

def _validateFloat(value, valueName):
    try:
        float(value)
    except ValueError:
        return {
            'status' : '400',
            'message' : 'expected '+ valueName + ' to be a float value.'
        }     

def validateFloats(dictionary, values):
    for arg in values:
        errorMessage = _validateFloat(dictionary.get(arg), arg)
        if errorMessage:
            return errorMessage  
       
def missingInformationError(valueName):
    return {
        'status' : '400',
        'message' : 'expected '+ valueName + ' to be supplied.'
    }
    