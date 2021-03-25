import ast
import os
import sys
from itertools import islice

from error import fs_corrupted;
from bcolors import *


# Import RAM
import ram

# Import dgb
import dbg

dic_locs = {}

print("Please enter the name of file system which needs to be started. ",end="")
print(f"{bcolors.OKCYAN}DONT FORGET EXTENSION (.txt){bcolors.ENDC}\nYou would have used this name while you ran {bcolors.WARNING} initialize_fs.py {bcolors.ENDC}")
fname = input()
ram.current_fileSystem = fname




def read_dict(txt_dict):
    return ast.literal_eval(txt_dict)

def read_master_block(fname):
    line_no = 0
    with open(fname, "r") as f:
        for line in islice(f,1,2):
            try:
                ram.master_block = read_dict(line);
            except:
                fs_corrupted()
                return
            break

def read_mbr(fname):
    mbr_str  = read_content(fname, [ram.master_block["mbr"][0],ram.master_block["mbr"][1]])
    ram.mbr = read_dict(mbr_str[0])

def read_fbbg(fname):
    free_blocks_str = read_content(fname,[ram.master_block["fbbg"][0],ram.master_block["fbbg"][1]])
    for str in free_blocks_str:
        ram.free_blocks.extend([int(x) for x in str.split()])



def read_ibg(fname):
    ram.inode_table  = read_content(fname, [ram.master_block["ibg"][0],ram.master_block["ibg"][1]], inode=True)
    global dic_locs
    for i in range(len(ram.inode_table)):
        ram.inode_table[i][0] = int(ram.inode_table[i][0]);
        ram.inode_table[i][1] = int(ram.inode_table[i][1]);
        ram.inode_table[i][3] = int(ram.inode_table[i][3])
        ram.inode_table[i][-1] =[int(x) for x in  ram.inode_table[i][-1].split('_')]
        if ram.inode_table[i][1] == 0 and ram.inode_table[i][-1][0] != -1:
            for j in range(len(ram.inode_table[i][-1])):
                dic_locs[str(ram.inode_table[i][-1][j])] = True;

def read_dbg(fname):
    if len(dic_locs) == 0:
        return
    rang = [int(ram.master_block['ibg'][1])+1,float('inf')];
    content = [];
    with open(fname, "r") as f:
        for i, line in enumerate(f):
            if i < rang[0]:
                continue
            if i > rang[1]:
                break
            if str(i-rang[0]) in dic_locs:
                content.append(read_dict(line))
            else:
                content.append(line[0:])

    dbg.data = content;

def read_content(fname, range, inode=False):
    content = [];
    with open(fname, "r") as f:
        for i,line in enumerate(f):
            if i<range[0]:
                continue
            if i>range[1]:
                break
            if inode:
                content.append((line[0:-1]).split())
            else:
                content.append(line[0:-1])


    return content;



def read_settings(fname):
    settings_str  = read_content(fname, [0,0])
    ram.settings = read_dict(settings_str[0])




def mount():

    if not os.path.exists(fname):
            # or raise error for not yet having partition
        fs_corrupted()
        return
    else:
        read_settings(fname);
        read_master_block(fname)
        read_mbr(fname)
        read_fbbg(fname)
        read_ibg(fname)
        read_dbg(fname)
        ram.out_scope_block = len(ram.inode_table)-1





