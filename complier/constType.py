from util import allTrue, firstFalse, isNum

def string2Const(text : str):
    assert len(text) > 0
    
    # case 0___
    if allTrue(text, isNum) and text[0] == '0':
        #print(allTrue(text, isNum))
        #i = allTrue(text, lambda x : x == '0')
        #if i != True:
        #    return int(text(i))
        return int(text)
    
    # string
    if len(text) == 3:
        return ord(text[1])
    elif len(text) >= 2:
        if text[0] == '"' and text[-1] == '"':
            return text[1:-1]
    
    
    return eval(text)