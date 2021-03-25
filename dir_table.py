import ram
import dbg
from error import file_not_a_dir

def get_dir_table(inode):
    dir_table = {}
    if ram.inode_table[inode][9][0] == -1 or len(ram.inode_table[inode][9])==0:
        return dir_table
    if ram.inode_table[inode][1] == 1:
        file_not_a_dir()
        return
    if len(dbg.data) != 0:
        for i in range(len(ram.inode_table[inode][9])):
            dir_table.update(dbg.data[ram.inode_table[inode][9][i]])
        return dir_table
    else:
        return {}