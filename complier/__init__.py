from enum import Enum

import complier.operator as Oper
from util import find_list_idx, find_sym_reverse, debug_recursive 
from util import firstFalse, firstTrue, allTrue
from util import isNum, isWord
from complier.constType import string2Const

class SubString:
    def __init__(self, text, start = 0, end = None):
        self.text = text
        self.start = start
        self.end = end if end != None else len(text)
        
    def __len__(self):
        return self.end - self.start
    
    def __str__(self):
        return self.text[self.start: self.end]
    
    
class Sentence:
    def __init__(self):
        self.operator = 0
        self.args = []
        self.original_text = ""
        
class macro:
    def __init__(self) -> None:
        self.name = ""
        self.argc = 0
        
        
keyWords = [
    "char","double","enum","float","int","long" ,"short" ,"signed","struct","union","unsign","void",
    "for","do","while","break","if","else","goto","switch","case","default","return",
    "auto","extern","register","static","const","sizeof","typedef","volatile"
]   
 
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
    
    

class SecntenceNode:
    def __init__(self) -> None:
        self.operator = None
        self.args = [] #list[SecntenceNode]

def parse_expr(symbol_list:list[str]):
    pass


class SymbolType(Enum):
    KeyWord = 0
    Split = 1
    Constant = 2
    Variable = 3
    Operator = 4
    #Debug = 5

def check_symbol_type(sym : str):
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
                   "?:","*=","+=","-=","/=","%=","&=","^=","|=","<<=",">>="]:
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

class FuncNode:
    def __init__(self) -> None:
        pass
    def compute(self,args = []):
        pass
        
class SenNode:
    def __init__(self,symbol_list : list, op) -> None:
        assert type(symbol_list) == list, symbol_list
        assert type(op) == str or op == None
        self.symbol_list = symbol_list
        self._op = op
        
    @property
    def op(self):
        return self._op
    
    def __str__(self) -> str:
        if self.op == None:
            return "[|"+str(self.symbol_list)[1:]
        #print(self.op, str(self.symbol_list))
        return  f"['{self.op}' | " + str(self.symbol_list)[1:]
        #return  str( [self.op] + self.symbol_list)
    def __len__(self):
        return len(self.symbol_list)
    def __iter__(self):
        self.i = 0
        return self
    def __next__(self):
        if self.i < len(self.symbol_list):
            res = self.symbol_list[self.i]
            self.i += 1
            return res
        else:
            raise StopIteration
    def __repr__(self) -> str:
        return str(self)    
    def __getitem__(self, i):
        return self.symbol_list[i]
    
    def __eq__(self, __value) -> bool:
        if type(__value) != type(self):
            return False
        if self.symbol_list != __value.symbol_list:
            return False
        if self.op != __value.op:
            return False
        return True
    
    def is_leaf(self):
        #if (self.op == None) and len(self.symbol_list) == 1:
        #    return type(self.symbol_list[0]) == str
        return False
    def leaf_val(self):
        assert self.is_leaf()
        return self.symbol_list[0]
    
    def print(*args, **kwargs):
        print(*args, **kwargs)
    
    def show_rule_1(self, tabNum = 0):
        if self.op == None:
            SenNode.show(self.symbol_list,tabNum = tabNum)
        elif self.op in "([":
            SenNode.print_format(self.op)
            SenNode.show(self.symbol_list,tabNum = tabNum)
            SenNode.print_format(Symbol_Split_map[self.op])
        elif self.op == '{':
            SenNode.print_format(self.op, nextLine = True, tabNum = tabNum + 1)
            SenNode.show(self.symbol_list, tabNum = tabNum + 1)
            SenNode.print_format('',nextLine = True, tabNum = tabNum)
            SenNode.print_format(Symbol_Split_map[self.op], tabNum = tabNum)
        elif self.op in ";":
            SenNode.show(self.symbol_list,tabNum = tabNum)
            SenNode.print_format(self.op)
        else:
            SenNode.show(self.symbol_list,tabNum = tabNum)
    visit_for = False
    def show_rule_2(self, tabNum = 0, for_semicolon = False):
        print('visit_for =',SenNode.visit_for)
        start_w = ''
        end_w = ''
        Indent = False
        
        nextLine_start = False
        nextLine_end = False
        
        if self.op == None:
            pass
        elif self.op in "([{":
            start_w = self.op
            end_w = Symbol_Split_map[self.op]
            if self.op == '{': 
                Indent = True
                nextLine_start = True
        elif self.op in ";":
            end_w = self.op
            if self.visit_for == False:
                nextLine_end = True
        elif self.symbol_list[0] == 'for':
            SenNode.print_format('for')
            SenNode.show(sym[1],tabNum = tabNum)
            SenNode.show(sym,tabNum = tabNum)
        
        SenNode.show(start_w, tabNum = tabNum)
        if nextLine_start:
            SenNode.print_format('',nextLine = True, tabNum = tabNum) 
        
        tmp_visit_for = False
        for sym in self.symbol_list:
            SenNode.show(sym,tabNum = tabNum)
            
            
            if sym == "for":
                SenNode.visit_for = True
                tmp_visit_for = True
        if tmp_visit_for == True:
            SenNode.visit_for = False
            
        SenNode.show(end_w, tabNum = tabNum)
        
        if nextLine_end:
            SenNode.print_format('',nextLine = True, tabNum = tabNum)        

    def print_format(text, tabNum = 0, nextLine = False):
        end_char = ''
        if nextLine == True:
            end_char = '\n' + "    "*tabNum
        SenNode.print(text, sep='', end = end_char)
    def show(symbol, tabNum = 0, for_semicolon = False):
        #print('tabNum', tabNum, symbol)
        if type(symbol) == list:
            #print('Error :',symbol)
            raise('show error')
            #for sym in symbol:
            #    SenNode.show(sym, tabNum = tabNum)
        elif type(symbol) == SenNode :
            #rint('-7')
            #rint(symbol)
            symbol.show_rule(tabNum = tabNum, for_semicolon = for_semicolon)
        else:
            #print('-8')
            SenNode.print_format(symbol, tabNum = tabNum)
            
    def check_function(self):
        if len(self) == 2:
            if self.symbol_list[0].is_leaf() == False:
                return False
            if check_symbol_type(self.symbol_list[0].leaf_val())  != SymbolType.Variable:
                return False
            if type(self.symbol_list[1]) != SenNode:
                return False
            if self.symbol_list[1].op == '(':
                return True
        return False
             
    
    def compute(self, vars = dict()):
        assert type(vars) == dict
        #print(self, self.op, self.is_leaf())
        
        if self.is_leaf():
            a0 = self.symbol_list[0]
            t0 = check_symbol_type(a0)
            #print("leaf : ",a0 ,t0)
            if t0 == SymbolType.Constant:
                return string2Const(a0)
            elif t0 == SymbolType.Variable:
                assert a0 in vars, f"{a0}  {vars}"
                return vars[a0]
            else:
                return a0  
        #
        # function
        #
        #print("-3")
        if self.check_function():
            #print("-4")
            
            #
            #  key word function
            #
            func_name = self.symbol_list[0].leaf_val()
            if func_name == "if":
                assert len(self) >= 2
                if self.symbol_list[2].op == '{':
                    if self.symbol_list[1].compute(vars = vars) == 1:
                        #self.symbol_list[2].compute(vars = vars)
                        pass
                elif self.symbol_list[2].op == ';':
                    pass
                else:
                    raise()
                return None
                
            if func_name == "while":
                pass
            #  TODO : others key worf function, like for, switch
            else: 
            #
            # self-define functions
            #
                assert func_name in vars, f"{func_name}  {vars}"
                
                args = [w.compute(vars = vars) for w in self.symbol_list[1].symbol_list]
                #print('args= ', args)
                return vars[func_name](*args)
                #if func_name
            

        #
        # split operator, ex. ( [ {
        #
        if (self.op in [None, '(','[','{']) or check_symbol_type(self.op) != SymbolType.Operator:
            if len(self.symbol_list) == 1:
                return self.symbol_list[0].compute(vars = vars)
            for w in self.symbol_list:
                assert type(w) == SenNode, w
                w.compute(vars = vars)
            return None
        
        #
        # uinary operator, ex. ~ ! 
        #
        if self.op in Oper.uinary_oper_compute.keys():
            a0 = self.symbol_list[0].compute(vars = vars)
            return Oper.uinary_oper_compute[self.op](a0)

        assert len(self.symbol_list) == 2, self.symbol_list
        
        #
        # binary operator, ex. + - * /  
        #
        if self.op in Oper.binary_oper_compute.keys():
            a0 = self.symbol_list[0].compute(vars = vars)
            a1 = self.symbol_list[1].compute(vars = vars)
            return Oper.binary_oper_compute[self.op](a0, a1)
        #
        # assign operator, ex. = += *= 
        #
        elif self.op in ['='] + list(Oper.assign_binary_oper.keys()):
            a0 = self.symbol_list[0].leaf_val()
            a1 = self.symbol_list[1].compute(vars = vars)
            assert check_symbol_type(a0) == SymbolType.Variable
            #print(a0)
            assert a0 in vars, f"{a0}  {vars}"
            if self.op == '=':
                vars[a0] = a1
            else: # in Oper.assign_binary_oper.keys()
                b = Oper.binary_oper_compute[Oper.assign_binary_oper[self.op]](vars[a0], a1)
                vars[a0] = b
            return vars[a0]


class SenLeaf(SenNode):
    def __init__(self, sym : str):
        super().__init__([sym], None)
    
    def is_leaf(self):
        return True
    
    @property
    def val(self):
        return self.symbol_list[0]
    
    def __eq__(self, __value) -> bool:
        if type(__value) == str:
            return self.val == __value
        else:
            return super().__eq__(__value)

#def SenLeaf(sym : str):
#    assert type(sym) == str
#    senNode = SenNode([sym], None)
#    senNode = SenNode([sym], None)
#    assert senNode.is_leaf() == True
#    return senNode
#
def check_node(senNode : SenNode):
    #print(senNode)    
    assert type(senNode) == SenNode, senNode
    assert type(senNode.symbol_list) == list , senNode

    if senNode.is_leaf():
        return 
    else:
        for w in senNode.symbol_list:
            check_node(w)

def check_build_split(senNode : SenNode):
    #print(senNode)    
    
    if type(senNode) == SenLeaf:
        assert len(senNode.symbol_list) == 1
        assert senNode.op == None
        assert type(senNode.symbol_list[0]) == str
        return           
    elif type(senNode) == SenNode:
        if len(senNode.symbol_list) == 1 and senNode.op == None:
            raise('no reduce')
    
        for w in senNode.symbol_list:
            check_build_split(w)
    else:
        raise()
            

def build_split(symbol_list : list):
    ''' create nodes by split symbols, ()[]{}. '''
    res = []
    for w in symbol_list:
        print(w,res)

        if w in [')',']','}']:
            rw = Symbol_Split_map[w]
            idx = find_list_idx(res, rw, reverse=True)
            assert idx >= 0
            res = res[:idx] + [SenNode(res[idx + 1:],rw)]
            
        elif w in [';',',']:
            f = lambda s : s.op == w if type(s) == SenNode else s == w
            idx = firstTrue(res, f, reverse=True) + 1
            res = res[:idx] + [SenNode(res[idx:],w)]
                
        else:
            res.append(w)
        
    senNode = SenNode(res, None)
    senNode = format_node(senNode)
    senNode = reduce_node(senNode)
    return senNode

def format_node(sym) -> SenNode:
    print(sym, type(sym))
    #debug_recursive(10)
    if type(sym) == str:
        return SenLeaf(sym)
    
    if type(sym) == SenNode:
        res = [format_node(w) for w in sym.symbol_list]
        op = sym.op
    elif type(sym) == list:
        res = [format_node(w) for w in sym]
        op = None
    else:
        raise()
    
    return SenNode(res,op)

def reduce_node(senNode : SenNode) -> SenNode:
    assert type(senNode) == SenNode
    if len(senNode) == 1 and senNode.op == None and (not senNode.is_leaf()):
        if type(senNode.symbol_list[0]) == SenNode:
            return senNode.symbol_list[0]
    
    return senNode
    

    
    
    
     

def build_split_1(symbol_list : list, skip_semicolon = False):
    ''' create nodes by split symbols, ()[]{}. '''
    
    #print(symbol_list)
    
    if len(symbol_list) == 1:
        return symbol_list
    
    next_step = False
    # scan ,;
    cnt_sym_split = {
        '(' : 0, '[' : 0, '{' : 0
    }
    res_list = []
    
    last_i = 0
    last_w = None
    for i, w in enumerate(symbol_list):
        if w in Symbol_Split:
            cnt_sym_split[w] += 1
        elif w in Symbol_Split_rev:
            cnt_sym_split[Symbol_Split_map[w]] -= 1
        #print(w, cnt_sym_split,sum(cnt_sym_split.values()))
        if (w in  ",;") and (sum(cnt_sym_split.values()) == 0):
            res_list.append(SenNode(symbol_list[last_i : i], w))
            last_i = i+1
            last_w = w
            
    if last_i != len(symbol_list):
        if len(res_list) == 0:
            assert last_i == 0
            next_step = True
        else:
            
            assert last_w != None
            res_list.append(SenNode(symbol_list[last_i : ], last_w))
        
    #print(res_list)
    #print('-1')
    #print("next_step =", next_step)
    if next_step == False:
        if len(res_list) == 1:
            return build_split(res_list[0])
        else:
            return SenNode([build_split(ls, skip_semicolon = True) for ls in res_list], None)
    
    # scan (){}[]
    idx_start = find_list_idx(symbol_list, Symbol_Split)
    #print(symbol_list, idx_start)
    #print('-2',idx_start)    
    if idx_start == -1: # no (){}[]
        if type(symbol_list) == list:
            return symbol_list
        elif type(symbol_list) == SenNode:
            return symbol_list
        else:
            raise('')
    else:
        #
        # found (){}[]
        # ex. 
        #    case I : 
        #       "a(b)c"  -> [a,[b],c]
        #       "a(b)"   -> [a,[b]]
        #       "(b)c"   -> [[b],c]
        #    case II:
        #       "(a)"    -> [a]
        # 
               
        sp = symbol_list[idx_start]
        idx_end = find_sym_reverse(symbol_list[idx_start + 1:],Symbol_Split_map[sp], sp)
        idx_end += idx_start + 1
        #print('-3',idx_start, idx_end)
        #print(symbol_list[:idx_start], symbol_list[idx_start + 1:idx_end], symbol_list[idx_end+1:])
        
        res = []
        if idx_start > 0:
            #res += build_split(symbol_list[:idx_start])
            ls = build_split(symbol_list[:idx_start])
            if type(ls) == list:
                res += ls
            else:
                res.append(ls)
            
        res.append(SenNode([build_split(symbol_list[idx_start + 1:idx_end])],sp))
        
        if idx_end + 1 < len(symbol_list):
            ls = build_split(symbol_list[idx_end+1:])
            if type(ls) == list:
                res += ls
            else:
                res.append(ls)
            
        if type(symbol_list) == SenNode:
            res = SenNode(res, symbol_list.op)
        
        #print('>>', res)
        if len(res) == 1: #case I
            return res[0]
        else:             #case II
            return res
     
            
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

def build_oper(senNode : SenNode):
    pass

def build_oper_1(sym_list):
    
    # judge class
    IsNode = False
    if type(sym_list) == SenNode:
        senNode = sym_list
        sym_list = senNode.symbol_list
        IsNode = True
    
    if type(sym_list) == str:
        #return SenLeaf(senNode)
        return SenLeaf(sym_list)
    
    if type(sym_list) == list:
        if len(sym_list) == 1:
            if type(sym_list[0]) == str:
                return SenLeaf(sym_list[0])
    

    #
    # process operators
    #
    
    #print('-1')
    NoOp = True
    op = None
    res_list = []    
    if len(sym_list) > 0:
        # binary operator
        for op_list in Oper.oper_oreder_table:
            idx = find_list_idx(sym_list, op_list, reverse= True)
            #print(idx)
            if idx != -1:
                op = sym_list[idx]
                #print('op=',op)
                #print('-1.1')
                res_list = [
                    build_oper(sym_list[:idx]),build_oper(sym_list[idx+1:])
                ]
                assert type(res_list[0]) == SenNode
                assert type(res_list[1]) == SenNode
                
                NoOp = False

        # uinary operator
        for op_list in ['!']:
            idx = find_list_idx(sym_list, op_list, reverse= True)
            print(idx, sym_list)
            if idx != -1:
                #res_sen = SenNode([
                #    build_oper(senNode[idx+1])
                #], op)
                op = sym_list[idx]
                res_list = [
                    build_oper(sym_list[idx+1])
                ]
                assert type(res_list[0]) == SenNode
                NoOp = False
    
    #
    # final
    #
    if NoOp == True:
        #print('-2')
        #sym_list = SenNode([build_oper(w) for w in sym_list], None)
        res_list = [build_oper(w) for w in sym_list]
        #print('>>',res_list)
        
        if IsNode == True:
            assert type(senNode) == SenNode
            #print(senNode.op)
            senNode.symbol_list = res_list
            if len(res_list) == 1:
                assert type(res_list[0]) == SenNode;
                if res_list[0].op == None and res_list[0].is_leaf() == False:
                    senNode.symbol_list = res_list[0].symbol_list
                
            return senNode
        else:
            return SenNode(res_list, op)
    else:
            
        #print('-3', IsNode, op)
        
        assert type(res_list) == list
        if IsNode == True:
            assert type(senNode) == SenNode
            #print(senNode.op)
            senNode.symbol_list = [SenNode(res_list, op)]
            return senNode
        else:
            return SenNode(res_list, op)
    

    
    
    
        

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
    if check == True:
        check_node(senNode)
    return senNode