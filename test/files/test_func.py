import sys, os

SCRIPT_DIR = os.getcwd() + '/complier'
sys.path.append(os.path.dirname(SCRIPT_DIR))


from complier import parse_words, build_split, build_oper, SenNode
from complier import check_node, check_build_split
from complier import FuncNode

def creat_func(func):
    assert callable(func)
    
    funcNode = FuncNode()
    


if __name__ == '__main__':
    #text = ''
    
    text = "b+=f(1000, 20);"
    #text = "10,20"
    symbol_list = parse_words(text)
    print("words : ",symbol_list)
    #sys.exit()
    
    senNode = build_split(symbol_list)
    print(senNode)
    #sys.exit()
    print("-1---------------------")
    check_build_split(senNode)
    senNode = build_oper(senNode)
    print(senNode)
    
    print("-2---------------------")
    check_node(senNode)
    #sys.exit()
    
    vars={
        'f' : lambda x,y : x*y,
        'b' : 15
    }
    print(vars)
    print(senNode.compute(vars))
    print(vars)