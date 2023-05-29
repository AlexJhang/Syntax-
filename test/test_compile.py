import sys, os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

#print(sys.path)

from complier import parse_words, build_split, build_oper, SenNode
from complier import check_node, check_build_split



if __name__ == '__main__':
    #text = ''
    
    #text = "(5)"
    #text = 'b*=1+2*3'
    #text = "3 + 6"
    #text = "if(a){i+=1;}else{i-=1;}"
    #text = "if(true){a+=1;b+=1;}"
    text = "(a b c)"
    #text="{a+=1;b+=1;}"
    symbol_list = parse_words(text)
    print("words : ",symbol_list)

    senNode = build_split(symbol_list)
    print(senNode)
    #sys.exit()
    print("-1---------------------")
    check_build_split(senNode)
    senNode = build_oper(senNode)
    print(senNode)
    
    print("-2---------------------")
    check_node(senNode)
    sys.exit()
    
    vars={
        'a' : 10,
        'b' : 15
    }
    print(vars)
    print(senNode.compute(vars))
    print(vars)