# RAM contains information read from Settings Block group, MBG, FBG, MBRBG and IBG


import math

# Address space read from hard disk once
# Master Block Group
global master_block
global mbr

"""
                                    MAKE IT TO VARY TO HANDLE ISSUR IN UNIX FILE SYSTEM REGARDING MEMORY USAGE

"""
out_scope_block = float('inf')


"""
                                    STAYS CONSTANT IN SPECIFIC FILE SYSTEM

"""
# Size/threshold/limit settings read from hard disk once
global directory_dictory_limit_per_block
directory_dictory_limit_per_block = 2

# Threshold defines how many direcotry dictionary can be in one block of dbg
threshold = directory_dictory_limit_per_block

global block_size
block_size = 4096
global int_size
int_size = 342

settings = {"threshold":threshold, "block_size":block_size, "int_size":int_size}

# Below commented might potentially be useless
# global disk_size
# disk_size = 50;
# global inode_entries
# inode_entries = 0




global ints_per_block
ints_per_block = math.floor(block_size / int_size)


# Inode ranges for each disc
global inode4disks
inode4disks = {};





"""
                                    Updated frequently by file system

"""


# CRITICAL
# Free blocks heap read from hard disk once
global free_blocks
free_blocks = []



# Inode info read from hard disk once
global current_inode
current_inode = 0;



# CRITICAL
# Inode Table
inode_table = []






# Parent Directory Inode
# parent = "root"
# parents_stack = []










# Open file table, for only non threaded operations

oft = {}


# Threads
threads_queue = {}


# thread queue flag
# semaphore = 0

# opened file - finode : [semaphore, method/object]
ofp_count = {}

# threads names
threads_names = {"cmakeFile":0,"cOpen":0, "trwt":0}


# threads output buffer
threads_output = []


# WORKING
# Add threads_output in userspace


# User space
# Will contain current_inode and parents stack.
user_space = {}


# changes happendes since last update
changes = 0

# changes_threshold
changes_threashold = 1

# current filesystem name
current_fileSystem = ""