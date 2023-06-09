import sys, os

SCRIPT_DIR = os.getcwd() + '/complier'
sys.path.append(os.path.dirname(SCRIPT_DIR))

from complier import SenNode
from complier import parse_words, build_node


TestCase = [
    ("1+1",2),
    ("10*90",900),
    ("(-1)*(-1)",1),
    ("2*3+8*7", 62),
    ("(1+2)*7", 21),
    ("6/3*5",10),
    ("7>>2",1),
    ("65520&31",16)
]

def compute(text):
    symbol_list = parse_words(text)
    senNode = build_node(symbol_list)
    
    vars = {}
    return senNode.compute(vars = vars)
     


if __name__ == '__main__':
    

    i = 0
    for text, val_true in TestCase:
        print(f"\n case {i}\n")
        
        print("words : ",text)
        
        val = compute(text)
        
        res = val_true == val
        
        print('compute :',val)
        print('true    :',val_true)
        
        if res == False:
            print('=== FAIL ===')
            break
        
        i+=1
    if i == len(TestCase):
        print('=== PASS ===')
    print(SCRIPT_DIR)