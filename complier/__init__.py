from enum import Enum

import complier.operator as Oper
from util import find_list_idx, find_sym_reverse, debug_recursive 
from util import firstFalse, firstTrue, allTrue
from util import isNum, isWord
from complier.symbolType import string2Const, check_symbol_type, SymbolType
from complier.senNode import SenNode, CtlNode, SenLeaf, OperNode

class SubString:
    def __init__(self, text, start = 0, end = None):
        self.text = text
        self.start = start
        self.end = end if end != None else len(text)
        
    def __len__(self):
        return self.end - self.start
    
    def __str__(self):
        return self.text[self.start: self.end]
    
class Buf_text:
    def __init__(self, output : list) -> None:
        self.buf = ""
        self.output = output
    def __add__(self, c):
        self.buf += c
        return self
    def refresh(self):
        if self.buf == "":
            return
        self.output.append(self.buf)
        self.buf = ""
    

def parse_words_split(text : str) -> list:
    symbol_list = []
    buf_text = Buf_text(symbol_list)
    
    
    class Status(Enum):
        Normal = 0
        Var = 1
        Operator = 2
        
    status = Status.Normal
    
    for c in text:
        #print(c, buf_text)
        if c == ' ':
            buf_text.refresh()
        elif c == ',':
            if status == Status.Var:
                tmp_isNum = True
                for cc in buf_text.buf:
                    if isNum(cc) or (cc in ".,"):
                        pass
                    else:
                        tmp_isNum = False
                if tmp_isNum == True:
                    buf_text += c
                else:
                    buf_text.refresh()
                    symbol_list.append(c)
        elif c in "(){}[];":
            buf_text.refresh()
            symbol_list.append(c)
        elif c in "!+-*/<>|&=~?:":
            if status == Status.Operator or status == Status.Normal:
                pass
            else :
                buf_text.refresh()
                
            buf_text += c
            status = Status.Operator
        else:
            if status == Status.Var:
                pass
            elif status == Status.Normal:
                pass
            else :
                buf_text.refresh()
            buf_text += c
            status = Status.Var
            
    buf_text.refresh()    
    return symbol_list

def parse_words(text : str) -> list:
    symbol_list = parse_words_split(text)
    
    res_list = []
    #print(symbol_list)
    for w in symbol_list:
        #print(w)
        if check_symbol_type(w) == None:
            if w[-1] == ',':
                res_list.append(w[:-1])
                res_list.append(',')
            else:
                raise()
        else:
            res_list.append(w)
                
        
    return res_list
    
            
def find_code_region(symbol_list : list):
    if symbol_list[0] == '{':
        return find_sym_reverse(symbol_list[2:],')','(')
    
    for i, w in enumerate(symbol_list):
        if w == ';':
            return i
        return -1


Symbol_Split_map = {
    '(' : ')',
    '[' : ']',
    '{' : '}',
    ')' : '(',
    ']' : '[',
    '}' : '{',
}
Symbol_Split = ['(','[','{']
Symbol_Split_rev = [')',']','}']



def check_node(senNode : SenNode):
    #print(senNode)    
    assert isinstance(senNode, SenNode), senNode
    assert type(senNode.args) == list , senNode

    if senNode.is_leaf:
        return 
    else:
        map(check_node, senNode)

def check_build_split(senNode : SenNode):
    #print(senNode)    
    
    if type(senNode) == SenLeaf:
        assert SenLeaf.check(senNode) == True
        return
    
    elif type(senNode) == SenNode:
        if len(senNode.args) == 1 and senNode.op == None:
            raise('no reduce')
        
        assert senNode.is_leaf == False
        
        map(check_build_split, senNode)
    else:
        raise()
            
def build_comma(senNode : SenNode) -> SenNode:
    sym_list = senNode.args
    for i,w in enumerate(sym_list):
        if type(w) != SenLeaf:
            sym_list[i] = build_comma(sym_list[i])
    
    last_idx = 0
    res=[]
    
    for i,w in enumerate(sym_list):
        if w in [';',',']:
            w = w.val
            res.append(SenNode(sym_list[last_idx:i],w))
            last_idx = i+1
            
    if last_idx == 0:
        return SenNode(sym_list, senNode.op)
    if last_idx < len(sym_list):
        res.append(SenNode(sym_list[last_idx:],None))
    return SenNode(res, senNode.op)
    
def build_split(symbol_list : list):
    ''' create nodes by split symbols, ()[]{}. '''
    res = []
    for w in symbol_list:
        #print(w,res)

        if w in [')',']','}']:
            rw = Symbol_Split_map[w]
            idx = find_list_idx(res, rw, reverse=True)
            assert idx >= 0
            res = res[:idx] + [SenNode(res[idx + 1:],rw)]
        else:
            res.append(w)
        
    senNode = SenNode(res, None)
    senNode = format_node(senNode)
    senNode = reduce_node(senNode)
    
    senNode = build_comma(senNode)
    #print('comma : ',senNode)
    senNode = format_node(senNode)
    senNode = reduce_node(senNode)
    
    return senNode

def format_node(sym) -> SenNode:
    '''
    format : every node is SenNode (include subclass)
    '''
    #print(sym, type(sym))
    #debug_recursive(10)
    if type(sym) == str:
        return SenLeaf(sym)
    if type(sym) == SenLeaf:
        return sym
    
    if type(sym) == SenNode:
        res = list(map(format_node, sym))
        op = sym.op
    elif type(sym) == list:
        res = list(map(format_node, sym))
        op = None
    else:
        raise()
    
    return SenNode(res,op)

def reduce_node(senNode : SenNode) -> SenNode:
    assert isinstance(senNode, SenNode)
    
    if senNode.is_leaf:
        return senNode
    
    
    #print('r ',senNode)
    if len(senNode) == 1 and senNode.op == None and (not senNode.is_leaf):
        if isinstance(senNode.args[0], SenNode):
            #print('rr')
            return reduce_node(senNode.args[0])
    
    senNode.map(reduce_node)
    return senNode
    
          
def create_nodes(symbol_list : list):
    if len(symbol_list) == 0:
        return
    
    ob = symbol_list[0]
    args = []
    if ob == "while":
        assert symbol_list[1] == '('
        idx = find_sym_reverse(symbol_list[2:],')','(')
        
        assert idx >= 0
        #print(idx)
        #print(symbol_list[2:idx+2])#arg[0]
        
        symbol_list = symbol_list[idx+3:]
        #print(symbol_list)
        #if symbol_list

def build_oper(senNode : SenNode) -> SenNode:
    
    if isinstance(senNode,SenLeaf):
        return senNode
    
    if len(senNode) == 0:
        return senNode  
    
    print(senNode)
    
    for node in [OperNode, CtlNode]:
        resNode = OperNode.check_create(senNode)
        if resNode != None:
            #print('>',resNode)        
            resNode.map(build_oper)
            
            return SenNode([resNode],senNode.op) if isinstance(senNode, SenNode) else resNode
    
    # no found type
    res_list =  list(map(build_oper,senNode))
    if type(senNode) == list:
        return SenNode(res_list, None)
    return SenNode(res_list, senNode.op)
    
        

def compile(text):
    
    # 1. parse words
    symbol_list = parse_words(text)
    print("words : ",symbol_list)
    
    # 2. word type
    #for w in symbol_list:
    #    print(f"{w:10}", (check_symbol_type(w)))
    
    print(build_split(symbol_list))
            

def compile_macro(text):
    pass

def build_node(symbol_list, check = True):
    senNode = build_split(symbol_list)
    if check == True:
        check_build_split(senNode)
    senNode = build_oper(senNode)
    senNode = reduce_node(senNode)
    if check == True:
        check_node(senNode)
    return senNode