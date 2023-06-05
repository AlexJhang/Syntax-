import sys, os

SCRIPT_DIR = os.getcwd() + '/complier'
sys.path.append(os.path.dirname(SCRIPT_DIR))

#print(sys.path)

from complier import check_symbol_type, keyWords, SymbolType

testCase_oper = [
    '*=',
    '-',
    '--',
    
]

testCase_con = [
    '0x30',
    '0x3F',
    '.56',
    '7.3',
    '0xabcdef',
    '0xABCDEF',
    '-1',
    '-0.1',
    '-.546',
    '5,500',
    '123,456.789',
    '-3,456.789',
    '0.123,456,7',
    '.123,456,7',
    '05',
    "'A'",
]

testCase_Var = [
    'a',
    'b1',    
    'Alex',
    'abc_aasfas_aga'
]

testCase_None = [
    'i++',
    '0.5.8',
    '0x3f6.7',
    '568A',    
    '#define',
    '><',
    '=>',
    '0xGG',
    'hi hi asfas',
    '---',
    '1,2345',
    '"0"',
    '"01"',
    
]

if __name__ == '__main__':
    print('[Test case keyWord]')
    for w in keyWords:
        t = check_symbol_type(w)
        if t != SymbolType.KeyWord:
            print(f"{w:10}", (check_symbol_type(w)))
    print()
    print('[Test case Operator]')
    for w in testCase_oper:
        print(f"{w:10}", (check_symbol_type(w)))
    print()
    print('[Test case Constant]')
    for w in testCase_con:
        print(f"{w:10}", (check_symbol_type(w)))
    print()
    print('[Test case Variable]')
    for w in testCase_Var:
        print(f"{w:10}", (check_symbol_type(w)))
    print()
    print('[Test case None]')
    for w in testCase_None:
        print(f"{w:10}", (check_symbol_type(w)))