from bcolors import *
import ram
from dir_table import get_dir_table


def ls(current_inode):
    current_dir = get_dir_table(current_inode)
    dirs = " "
    files = " "
    for fil in current_dir:
        if ram.inode_table[current_dir[fil]][1] == 0:
            dirs = dirs + fil + " ";
        else:
            files = files + fil + " ";

    # dirs on left of -
    return dirs + "-" + files


