from dir_table import get_dir_table

import ram


def chDir(file_name, current_inode, currentUser):

    if file_name == "..":
        if len(ram.user_space[currentUser][1]) == 0:
            return 0

        new_inode = ram.user_space[currentUser][1].pop(-1)
        ram.user_space[currentUser][0] = new_inode
        return 0

    dir_table = get_dir_table(current_inode)

    if file_name not in dir_table:
        # file_not_found()
        return -11


    new_inode = dir_table[file_name]
    if ram.inode_table[new_inode][1] == 0:
        ram.user_space[currentUser][1].extend([current_inode])
        ram.user_space[currentUser][0] = new_inode
        return 0
    else:
        # file_not_a_dir()
        return -5




