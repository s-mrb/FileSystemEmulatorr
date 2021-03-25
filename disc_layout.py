import math
# 4 4096 50


def mk_layout(settings, inode_entries, master_block, inode4disks , free_blocks ,ints_per_block,fname):
    with open(fname,"w+") as f:
        f.write( str(settings) + "\n" );
        f.write( str(master_block) + "\n" );
        f.write( str(inode4disks) + "\n" );

        blocks4free_blocks = math.ceil(len(free_blocks)/ints_per_block)
        for i in range(blocks4free_blocks):
            if i==blocks4free_blocks:
                f.write(' '.join(str(x) for x in free_blocks[i*ints_per_block:-1])+"\n")
            else:
                f.write(' '.join(str(x) for x in free_blocks[i*ints_per_block:(i+1)*ints_per_block])+"\n")
        inode_str = get_inode_str(root=True);
        f.write("0 "+inode_str+"\n")
        inode_str = get_inode_str();
        for i in range(inode_entries):
            f.write(str(i+1)+" "+inode_str+"\n")




def get_inode_str(root=False):
    if root:
        return "0 rwx 1 root nn nn nn 0 -1";
    else:
        return "-1 rwx 0 root nn nn nn 0 -1"
