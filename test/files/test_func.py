import sys, os

SCRIPT_DIR = os.getcwd() + '/complier'
sys.path.append(os.path.dirname(SCRIPT_DIR))

#from complier import SenNode
from complier import parse_words, build_node

conde_text  = '''

'''



def compute(text):
    symbol_list = parse_words(text)
    senNode = build_node(symbol_list)
    
    vars = {}
    return senNode.compute(vars = vars)




if __name__ == '__main__':
    print(SCRIPT_DIR)
    #print(ROOT_DIR)
    print(os.listdir())
    print(compute("(1+2)*7"))


