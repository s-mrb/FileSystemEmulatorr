import dbg
import ram

def update_file_link_n_parent_dir(filename,current_dir_inode):
    index ,length = -1, -1
    inode2traverse = -1

    # addr_list corresponding to current_inode, must contain dictionary for directory
    rang = len(ram.inode_table[current_dir_inode][9]);

    # this function should not run if len(data) == 0
    if len(dbg.data)!=0:

        # loop through addr_list
        for i in range(rang):

            # read dictionary corresponding to this index of addr_list
            temp = dbg.data[ram.inode_table[current_dir_inode][9][i]]

            # check if file exists in dictionary corresponding to this index of addr_list
            if filename in temp:

                # if file found then note its inode, for traversal use later
                inode2traverse = temp[filename]

                # note index of addr_list whose corresponding dictionary contain file
                index = i

                # get length of dictionary corresponding to this index of addr_list
                length = len(temp)
                if length > 1:
                    del temp[filename]
                    dbg.data[ram.inode_table[current_dir_inode][9][i]] = temp;
                    return inode2traverse
                else:
                    # its better to put it equal to small string
                    dbg.data[ram.inode_table[current_dir_inode][9][i]] = "x";

                    if len(ram.inode_table[current_dir_inode][9]) == 1:
                            ram.inode_table[current_dir_inode][9] = [-1]
                            return inode2traverse
                    ram.inode_table[current_dir_inode][9].pop(index)
                    return inode2traverse
    return  False

