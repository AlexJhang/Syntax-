

oper_oreder_table = [ # binary operator
    ['=', '+=', '-=', '*=', '/=', '%=', '&=', '^=', '|=', '<<=', '>>='],
    ['?',':'],
    ['||'],['&&'],['|'],['^'],['&'],
    ['==','!='],
    ['<','<=','>','>='],
    ['<<','>>'],
    ['+', '-'],
    ['*', '/', '%']
]

binary_oper_compute = {
    '+' : lambda a,b : a+b,
    '-' : lambda a,b : a-b,
    '*' : lambda a,b : a*b,
    '/' : lambda a,b : a/b,
    '%' : lambda a,b : a%b,
    '&&': lambda a,b : a&b,
    '||': lambda a,b : a|b,
    '<<': lambda a,b : a<<b,
    '>>': lambda a,b : a>>b,
}

#'+=', '-=', '*=', '/=', '%=', '&=', '^=', '|=', '<<=', '>>='],
assign_binary_oper = {
    '+='  : '+'  ,
    '-='  : '-'  ,
    '*='  : '*'  ,
    '/='  : '/'  ,
    '%='  : '%'  ,
    '&='  : '&'  ,
    '^='  : '^'  ,
    '|='  : '|'  ,
    '<<=' : '<<' ,
    '>>=' : '>>' ,
}

uinary_oper_compute = {
    '!' : lambda a: 0 if a > 0 else 1,
}