import sys, os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

#print(sys.path)

from complier import build_node, parse_words, SenNode, SenLeaf, CtlNode
from complier import check_node, check_build_split

def compile(text):
    return build_node(parse_words(text))

TestCase = [
    ("a b",SenNode([SenLeaf('a'), SenLeaf('b')],None)),
    ("a (b)",SenNode([SenLeaf('a'), SenNode([SenLeaf('b')],'(')],None)),
    ("a(b(c))",SenNode([SenLeaf('a'), SenNode([SenLeaf('b'), SenNode([SenLeaf('c')],'(')], '(')],None)),
    
    ("a+=1",SenNode([SenLeaf('a'), SenLeaf('1')],'+=')),
    ("a+=1;",SenNode([compile("a+=1")],';')),
    ("{a+=1;}",SenNode([compile("a+=1;")],'{')),
    ("a+=1;b+=1;",SenNode([compile("a+=1;"),compile("b+=1;")],None)),
    ("a+=1;b+=1",SenNode([compile("a+=1;"),compile("b+=1")],None)),
    ("{a+=1;b+=1;}",
        SenNode([
            SenNode([
                    SenNode([SenLeaf('a'), SenLeaf('1')],'+='),
                ],';'),
            SenNode([
                    SenNode([SenLeaf('b'), SenLeaf('1')],'+='),
                ],';'),
        ],'{')
     ),
    ("if(true){a+=1;b+=1;}",CtlNode([
        SenNode([SenLeaf('true')],'('),
        compile("{a+=1;b+=1;}")
        ],'if')),
    ("if(true){a+=1;b+=1;}else{return;}",SenNode([
        SenLeaf('if'),
        SenNode([SenLeaf('true')],'('),
        compile("{a+=1;b+=1;}"),
        SenLeaf('else'),
        SenNode([compile('return;')],'{')
        ],None)),
    ("f(0);",SenNode([SenLeaf('f'), SenNode([SenLeaf('0')],'(')],';')),
    ("while(1){};",SenNode([SenLeaf('while'), 
            SenNode([SenLeaf('1')],'('),
            SenNode([],'{')
        ],';'))
]

if __name__ == '__main__':

    i = 0
    for text, senNode_true in TestCase:
        print(f"\n case {i}\n")
        symbol_list = parse_words(text)
        print("words : ",symbol_list)
        
        senNode = build_node(symbol_list)
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
    