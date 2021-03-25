from bcolors import *
from dir_table import get_dir_table
import ram

def blocksConsumedByFile(filename, current_inode):
    filename = filename;
    dir_table = get_dir_table(current_inode)
    if filename in dir_table:
        return 0, ram.inode_table[dir_table[filename]][9]
    else:
        # file_not_found()
        return -11, -11



def freeBlocks():
    
    
    blocks_consumed = ram.free_blocks.count(ram.out_scope_block)
    blocks_left = len(ram.free_blocks) - blocks_consumed 
    return blocks_left



def showMasterBlock():
    mblock = ""
    for blockGroup in ram.master_block:
        mblock = mblock +"\t"+blockGroup+"\t\t"+str(ram.master_block[blockGroup]) + "\n"
    return mblock
