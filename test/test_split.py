import sys, os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

#print(sys.path)

from complier import build_node, parse_words, SenNode, SenLeaf
from complier import build_split, check_build_split

def compile(text):
    return build_node(parse_words(text))

TestCase = [
    #("a b; (c) d;",SenNode([],None)),
    
    ("a b",SenNode([SenLeaf('a'), SenLeaf('b')],None)),
    ("a (b)",SenNode([SenLeaf('a'), SenNode([SenLeaf('b')],'(')],None)),
    ("a(b(c))",SenNode([SenLeaf('a'), SenNode([SenLeaf('b'), SenNode([SenLeaf('c')],'(')], '(')],None)),
    
    ("f(0);",SenNode([SenLeaf('f'), SenNode([SenLeaf('0')],'(')],';')),
]

if __name__ == '__main__':

    i = 0
    for text, senNode_true in TestCase:
        print(f"\n case {i}\n")
        symbol_list = parse_words(text)
        print("words : ",symbol_list)
        
        senNode = build_split(symbol_list)
        check_build_split(senNode)
        
        print(senNode)
        
        print(senNode_true)
        res = senNode_true == senNode
        print(res)
        if res == False:
            print('=== FAIL ===')
            break
        
        i+=1
    if i == len(TestCase):
        print('=== PASS ===')
    #sys.exit()
    