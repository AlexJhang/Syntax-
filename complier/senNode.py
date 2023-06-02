from complier.symbolType import string2Const, check_symbol_type, SymbolType
import complier.operator as Oper

class SenNode:
    def __init__(self,symbol_list : list, op) -> None:
        assert type(symbol_list) == list, symbol_list
        assert type(op) == str or op == None, op
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
    
    @property
    def symList_op(self):
        return self.symbol_list, self._op
    
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
        ''' include function, if, while, ...'''
        if len(self) >= 2:
            if self.symbol_list[0].is_leaf() == False:
                return False
            if check_symbol_type(self.symbol_list[0].leaf_val())  not in [SymbolType.Variable, SymbolType.KeyWord] :
                return False
            if type(self.symbol_list[1]) != SenNode:
                return False
            if self.symbol_list[1].op == '(':
                return True
        return False
             
    
    def compute(self, vars = dict()):
        assert type(vars) == dict
        print(self, self.op, self.is_leaf())
        
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
                        self.symbol_list[2].compute(vars = vars)
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
                assert len(self) == 2
                if callable(vars[func_name]):
                    args = [w.compute(vars = vars) for w in self.symbol_list[1].symbol_list]
                    #print('args= ', args, func_name)
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
            t = Oper.uinary_oper_compute[self.op](a0)
            if self.op in ['++x','--x']:
                vars[self.symbol_list[0].val] = t
            return t

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
            print(a0,a1)
            assert a0 in vars, f"{a0}  {vars}"
            if self.op == '=':
                vars[a0] = a1
            else: # in Oper.assign_binary_oper.keys()
                b = Oper.binary_oper_compute[Oper.assign_binary_oper[self.op]](vars[a0], a1)
                vars[a0] = b
            return vars[a0]
