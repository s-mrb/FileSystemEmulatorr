
import math
import ram
import dbg



def makeFile(current_inode, filename, dir=True):
    newfile_inode = False
    file_type = 0 if dir else 1;

    # find inode for new file
    for i in range(len(ram.inode_table)):
        if ram.inode_table[i][3] < 1:
            newfile_inode = i;

            # update references
            ram.inode_table[i][3] = 1

            # update type
            ram.inode_table[i][1] = file_type
            break



    # get address_list of current directory
    addr_list = ram.inode_table[current_inode][9]


    # handle the case when addr_list[0] == -1
    if addr_list[0] == -1:
        addr_list = []

    # find index in addr_list for new data
    index = -1

    for i in range(len(addr_list)):
        if len(dbg.data[addr_list[i]]) < ram.settings["threshold"]:
            index = i;
            break;



    # if index found / there is element in the addr_list which could be filled
    if index > -1:
        dbg.data[addr_list[index]].update({filename:newfile_inode})
    else:
        new_address = ram.free_blocks.pop(0);
        addr_list.extend([new_address])
        ram.inode_table[current_inode][9] = addr_list
        ram.free_blocks.extend([ram.out_scope_block])
        ram.free_blocks.sort()

        if len(dbg.data) == new_address:
            dbg.data.extend([{filename:newfile_inode}])
        else:
            dbg.data[new_address] = {filename:newfile_inode}


