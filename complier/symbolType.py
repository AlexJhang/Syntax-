from util import allTrue, firstFalse, isNum
from enum import Enum
from util import isNum, isWord

def string2Const(text : str):
    assert len(text) > 0
    
    # case 0___
    if allTrue(text, isNum) and text[0] == '0':
        return int(text)
    
    # string
    if len(text) == 3:
        return ord(text[1])
    elif len(text) >= 2:
        if text[0] == '"' and text[-1] == '"':
            return text[1:-1]
    
    
    return eval(text)

keyWords = [
    "char","double","enum","float","int","long" ,"short" ,"signed","struct","union","unsign","void",
    "for","do","while","break","if","else","goto","switch","case","default","return",
    "auto","extern","register","static","const","sizeof","typedef","volatile"
]   

class SymbolType(Enum):
    KeyWord = 0
    Split = 1
    Constant = 2
    Variable = 3
    Operator = 4
    #Debug = 5


def check_symbol_type(sym : str):
    ''' return SymbolType '''
    if type(sym) != str:
        return None
    #SymbolType.KeyWord
    if sym in keyWords:
        return SymbolType.KeyWord
    #SymbolType.Split
    if sym[0] in "(){}[];,":
        if len(sym) == 1:
            return SymbolType.Split
        return None
    #SymbolType.Operator
    if sym[0] in "?!+-*/<>|&=":
        if len(sym) == 1:
            return SymbolType.Operator 
        if sym in ["++","--","<<",">>","<=",">=","==","!=","&&","||",
                   "?:","*=","+=","-=","/=","%=","&=","^=","|=","<<=",">>=",
                   "-x","++x","--x"]:
            return SymbolType.Operator
        
        if sym[0] == '-' and ((sym[1] == ".") or isNum(sym[1])):
            pass # maybe Constant, like -.5 -0.5 -1.5
            #return SymbolType.Debug
        else:
            return None
    
    #SymbolType.Constant
    # string
    if len(sym) >= 2:
        if sym[0] == "'" and sym[-1] == "'" and len(sym) == 3:
            return SymbolType.Constant
        elif sym[0] == '"' and sym[-1] == '"' and len(sym) == 3:
            return None
        elif sym[0] == '"' and sym[-1] == '"':
            return SymbolType.Constant
        
    # number
    if sym[0] in ".-" or isNum(sym[0]):
        # hex
        if len(sym) > 2:
            if sym[:2] in ["0x","0X"]:
                for c in sym[2:]:
                    if (not isNum(c)) and (c not in "abcdefABCDEF"):
                        return None
                return SymbolType.Constant
            
        #float and dec
        if sym[0] == '.' and len(sym) == 1:
            return None
        start_idx = 0
        if sym[0] == '-':
            start_idx = 1
        visit_point = False
        coma_list = []
        idx_point = None
        for i,c in enumerate(sym[start_idx:]):
            if c == '.':
                if visit_point:
                    return None
                visit_point = True
                coma_list.append(i)
                idx_point = i
            elif c == ',':
                coma_list.append(i)
            elif not isNum(c):
                return None
        
        # xxx,xxx,xxx case
        if idx_point == None:
            idx_point = len(sym) - start_idx
        #print(coma_list, idx_point,start_idx)        
        if len(coma_list) > 0 :
            coma_list = [ n - idx_point for n in coma_list]
        
            for n in coma_list:
                if n % 4 != 0:
                    return None
                
        return SymbolType.Constant
    
    #SymbolType.Variable
    if isWord(sym[0]):
        for c in sym[1:]:
            if c in "_":
                continue
            if (not isNum(c)) and (not isWord(c)):
                return None
        return SymbolType.Variable
    return None
