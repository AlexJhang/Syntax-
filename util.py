from enum import Enum
import re
import os

def remove_all_comment(input_lines : list):
    
    # degbug
    #vprint = print
    def vprint(*argc, **kwargs):
        pass

    class Mode(Enum):
        Normal = 0
        Comment = 1

    def remove_comment(line : str, arg):
        res_line = ""
        idx_comment_end = -2
        idx_comment_start = 0
        vprint(line)
        while True:
            vprint(idx_comment_start, idx_comment_end, res_line)
            idx_comment_start = line.find("/*",idx_comment_end+2)
            if idx_comment_start != -1:
                res_line += line[idx_comment_end+2:idx_comment_start]
            else:
                res_line += line[idx_comment_end+2:]
                break
            
            idx_comment_end = line.find("*/", idx_comment_start)
            if idx_comment_end != -1:
                pass
            else:
                arg[0] = Mode.Comment
                break
            
        return res_line
    
    i = 0
    mode = Mode.Normal
    res_line_list = []
    for line in input_lines:
        i += 1
        #line = str(line[:-2], "utf-8")
        line = line[:-2].decode("utf-8","ignore")
        
        res_line = ""

        vprint(f"line{i:5} :", mode, " ", line)

        if mode == Mode.Comment:
            idx_comment_end = line.find("*/")
            if idx_comment_end != -1:
                mode = Mode.Normal
                line = line[idx_comment_end+2:]
            else :
                pass
        
        if mode == Mode.Normal:
            arg = [mode]
            line = remove_comment(line, arg)
            mode = arg[0]

            if mode == Mode.Normal:
                idx_double_slash = line.find("//")
                if idx_double_slash != -1:
                    vprint(i, idx_double_slash)
                    res_line = line[:idx_double_slash]
                else :
                    res_line = line

        #wf.write(bytes(res_line, "utf-8"))
        #wf.write(b"\r\n")
        res_line_list.append(res_line)
    return res_line_list


def reduce_lines(input_lines : list):
    res_line_list = []
    
def lines_to_Code(input_lines : list, tar_path : str):
    
    with open(tar_path, 'wb')  as wf:
        for line in input_lines :
            wf.write(bytes(line, "utf-8"))
            wf.write(b"\r\n")
            
def find_all_file(dir_path : str, ext = ['c','h']):
    '''
    Args:
            ext: file extension.
    '''
    res_list = []
    for root, dirs, files in os.walk(dir_path):
        # Print the file names
        for file in files:
            #print(os.path.join(root, file))
            for ee in ext:
                if ee == '*':
                    #print(root, file)
                    res_list.append(root + "\\" + file)
                    break
                ee = '.'+ee
                if file[-len(ee):] == ee:
                    #print(root, file)
                    res_list.append(root + "\\" + file)
                    break
    return res_list

def split_mulit_blank(line : str):
    return [w for w in line.split(' ') if w != '']

def reduce_blank( line : str):
    return " ".join(split_mulit_blank(line))

def find_list_idx(symbol_list : list, Tar, reverse = False):
    '''
    Args:
        Tar:
            Type : 
                1. str 
                2. list(str) : multi tar
    '''
    if type(Tar) != list:
        Tar = [Tar]
    iter = enumerate(symbol_list) if reverse == False else enumerate(reversed(symbol_list))
    L = len(symbol_list)
    for i, w in iter:
        if w in Tar:
            if reverse == False:
                return i
            else:
                return L - i - 1
    return -1

def find_sym_reverse(symbol_list : list, sym_tar : str, sym_reverse : str):
    s = -1
    for i,w in enumerate(symbol_list):
        #print(w,s)
        if w == sym_reverse:
            s -= 1
        elif w == sym_tar:
            s += 1
        #print(s)symbol_list
        if s >= 0:
            return i
    return -1

def firstFalse(L : list, f):
    #assert type(f) == function
    '''
    return : 
        -1   : f(l) is True, for all l in L
        >=0  : index of the first False 
    '''
    for i, a in enumerate(L):
        if f(a) == False:
            return i
    return -1    

def allTrue(L : list, f):
    idx = firstFalse(L, f)
    if idx == -1:
        return True
    else:
        return False




def isNum(c):
    n = ord(c)
    return (n >= 48) and (n <= 57)

def isWord(c):
    n = ord(c)
    return ((n >= 97) and (n <= 122)) or ((n >= 65) and (n <= 90))

_debug_cnt = 0
def debug_recursive(max : int):
    global _debug_cnt
    _debug_cnt += 1
    assert _debug_cnt < max

def prefix_cmp(text : str, CmpStr : str) -> bool:
    l = len(CmpStr)
    if text[:l] == CmpStr:
        return True
    else:
        return False
