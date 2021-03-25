import math

import ram
import dbg
from error import file_not_a_dir,fname_not_in_dir;
from inode2traverse import update_file_link_n_parent_dir
from dir_table import get_dir_table


def move(fil1,fil2,parent_dir_inode):

    dir_table = get_dir_table(parent_dir_inode);
    if fil2 not in dir_table:
        # fname_not_in_dir();
        return -4;
        
    if fil1 not in dir_table:
        # fname_not_in_dir();
        return -4;
    fil2_inode = dir_table[fil2];
    
    if ram.inode_table[fil2_inode][1] != 0:
        # file_not_a_dir()
        return -5
    else:
        fil1_inode = update_file_link_n_parent_dir(fil1,parent_dir_inode);
        if fil1_inode == None:
            # fname_not_in_dir();
            return -4
        add_link2file(fil1,fil1_inode,fil2_inode);
        return 0


def add_link2file(file1, file1_inode, file2_inode):

    # get address_list of fil2
    addr_list = ram.inode_table[file2_inode][9]


    # handle the case when addr_list[0] == -1
    if addr_list[0] == -1:
        addr_list = []

    # find index in addr_list for new data
    index = -1

    for i in range(len(addr_list)):
        if len(dbg.data[addr_list[i]]) < threshold:
            index = i;
            break;



    # if index found / there is element in the addr_list which could be filled
    if index > -1:
        dbg.data[addr_list[index]].update({file1:file1_inode})
    else:
        new_address = ram.free_blocks.pop(0);
        addr_list.extend([new_address])
        ram.inode_table[file2_inode][9] = addr_list
        ram.free_blocks.extend([ram.out_scope_block])
        ram.free_blocks.sort()

        if len(dbg.data) == new_address:
            dbg.data.extend([{file1:file1_inode}])
        else:
            dbg.data[new_address] = {file1:file1_inode}




# move("public","xx",current_inode)


