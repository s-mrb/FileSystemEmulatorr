import ram
import dbg
import math

import copy

def hardWrite(fname):
    inode_string_table = ""
    ints_per_block = math.floor(ram.settings["block_size"]/ram.settings["int_size"])
    inode_table = copy.deepcopy(ram.inode_table)
    free_blocks = copy.deepcopy(ram.free_blocks)
    data = copy.deepcopy(dbg.data)

    for i in range(len(inode_table)):
        inode_table[i][-1] = '_'.join(str(x) for x in inode_table[i][-1]);
        inode_string_table = inode_string_table + ' '.join(str(x) for x in inode_table[i]) + "\n"
    with open(fname, 'w+') as f:
        f.write(str(ram.settings)+"\n");
        f.write(str(ram.master_block) + "\n");
        f.write(str(ram.mbr) + "\n");
        blocks4free_blocks = math.ceil(len(free_blocks) / ints_per_block)
        for i in range(blocks4free_blocks):
            if i == blocks4free_blocks:
                f.write(' '.join(str(x) for x in free_blocks[i * ints_per_block:-1]) + "\n")
            else:
                f.write(' '.join(str(x) for x in free_blocks[i * ints_per_block:(i + 1) * ints_per_block]) + "\n")
        f.write(inode_string_table + '\n'.join(str(x) for x in data))




