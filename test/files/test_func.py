import sys, os

SCRIPT_DIR = os.getcwd() + '/complier'
sys.path.append(os.path.dirname(SCRIPT_DIR))


from complier import parse_words, build_split, build_oper, SenNode
from complier import check_node, check_build_split
from complier import parse_file

def creat_func(func):
    assert callable(func)
    
    funcNode = FuncNode()
    


if __name__ == '__main__':
    print(parse_file('test/files/testcase/1.c'))