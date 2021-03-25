
import ram
import dbg

from create import makeFile
from move import move
from delete import deleteFile
from ls import ls
from chDir import chDir
from dir_table import get_dir_table

from OpenFile import Open
from hard_write import hardWrite
from memory import *
import threading
import time


def cmakeFile(current_inode, filename, dir=True):
    
    makeFile(current_inode, filename, dir)

    


# 0 = read mode, 1 = write mode,
def cOpen(fname, mode = 0, currentUser=None):
    name = fname
    if fname in ram.oft:
        return -13
    
    # left error on trying to open a file which do not exist
    # when read write operations are completed then it must be removed from open file table
    status, obj = Open(fname, ram.user_space[currentUser][0]);

    if status < 0:
        return status
    ram.oft[fname] = obj
    return 0



def cClose(fname):
    if fname in ram.oft:
        ram.oft.pop(fname)
        return 0
    return -12


def cread(fname, start, end):
    if fname in ram.oft:
        return 0 , ram.oft[fname].read(start, end);
    return -12, -12

def cwrite(fname, loc, text):
    if fname in ram.oft:
        status = ram.oft[fname].write(loc, text);
        return status
    else:
        return -12


def ctruncate(fname, size):
    if fname in ram.oft:
        status = ram.oft[fname].truncate(size);
        return status
    return -12




# methods, read = 0, write = 1, truncate = 2
def trwt( fname, method, current_inode, arguments ,currentUser, delay = 0):

    thread_data_title = fname + "  " + str(method)
    current_file_table = get_dir_table(current_inode)
    if fname not in current_file_table:
        return -4

    file_inode = current_file_table[fname]

    name = fname
    status, call = Open(fname, current_inode);
    oft_tname = str(file_inode) + "_t"
    if oft_tname not in ram.oft:
        ram.oft[oft_tname] = [0, call];
    
    if file_inode in ram.ofp_count:
        ram.ofp_count[file_inode] = ram.ofp_count[file_inode] + 1
    else:
        ram.ofp_count[file_inode] = 1

    if method == 0:
        while True:
            if ram.oft[oft_tname][0] == 0 :
                break
        start, end = arguments[0], arguments[1]
        t = threading.Thread(target=pread, args=(file_inode, start, end, thread_data_title, currentUser, delay),daemon=True)
        t.start()
        return 0

    if method == 1:
        # dont allow while semaphore 
        while True:
            if ram.oft[oft_tname][0] == 0:
                break
        loc, text = arguments[0], arguments[1]
        ram.oft[oft_tname][0] =  1

        t = threading.Thread(target=pwrite, args=(file_inode, loc, text, thread_data_title, currentUser, delay))
        t.start()
        return 0

    if method == 2:
        while True:
            if ram.oft[oft_tname][0] == 0:
                break
        size = arguments[0]
        ram.oft[oft_tname][0] =  1
        t = threading.Thread(target=ptruncate, args=(file_inode, size, thread_data_title,  currentUser, delay))
        t.start()
        return 0

    


def ptruncate(file_inode, size, thread_data_title, currentUser, delay):
    if delay > 0:
        time.sleep(delay)

    status = ram.oft[str(file_inode) + "_t"][1].truncate(size);
    ram.oft[str(file_inode) + "_t"][0] = 0
    ram.ofp_count[file_inode] = ram.ofp_count[file_inode] -1

    if ram.ofp_count[file_inode] == 0:
        ram.oft.pop(str(file_inode) + "_t")

    if status == -9:
        
        ram.user_space[currentUser][2].append(thread_data_title+"\n"+"Error Code -9")
        # trimming_empty_file()
        return 0

    if status == -12:
        ram.user_space[currentUser][2].append(thread_data_title+"\n"+"Error Code -12")
        # file_not_open();
        return 0
    ram.changes = ram.changes + 1
    return 0

def pwrite(file_inode,  loc, text, thread_data_title, currentUser, delay):
    if delay > 0:
        time.sleep(delay)
    status = ram.oft[str(file_inode) + "_t"][1].write(loc, text);
    
    ram.oft[str(file_inode) + "_t"][0] = 0
    ram.ofp_count[file_inode] = ram.ofp_count[file_inode] -1

    if ram.ofp_count[file_inode] == 0:
        ram.oft.pop(str(file_inode) + "_t")

    if status == -7:
        ram.user_space[currentUser][2].append(thread_data_title+"\n"+"Error Code -7")
        # free_space_not_found()
        return 0

    if status == -8:
        ram.user_space[currentUser][2].append(thread_data_title+"\n"+"Error Code -8")
        # out_of_scope_memory_accessed_in_file()
        return 0

    if status == -12:
        ram.user_space[currentUser][2].append(thread_data_title+"\n"+"Error Code -13")
        # file_not_open();
        return 0
    ram.changes = ram.changes + 1
    return 0

def pread( file_inode, start, end, thread_data_title, currentUser, delay):
    if delay > 0:
        time.sleep(delay)

    text = ram.oft[str(file_inode)+"_t"][1].read(start,end);
    ram.ofp_count[file_inode] = ram.ofp_count[file_inode] -1

    if ram.ofp_count[file_inode] == 0:
        ram.oft.pop(str(file_inode) + "_t")

    ram.user_space[currentUser][2].append(thread_data_title+"\n"+text)
    return 0




def cls(current_inode):
    return ls(current_inode)
    


def cshow_data(index):
    if index >= len(dbg.data):
        return -15, -15
    return 0,show_data(index)
    

def show_data(index):



    string_data = ""

    if index != -1:
        return str(dbg.data[index])

    for content in dbg.data:
        string_data = string_data + str(content) + "\n"

    return string_data


def cdelete(filename, current_inode):
    status = deleteFile(filename=filename, current_inode=current_inode)
    return status
    
def cmove(file1, file2, current_inode):
    status = move(file1, file2, current_inode)
    return status

def memmap(index):
    if index != -1:
        return str(ram.inode_table[index])
    mem_list_str = ""
    for li in ram.inode_table:
        mem_list_str = mem_list_str + str(li) + "\n"

    return mem_list_str

def cmemmap(index):
    if index >= len(ram.inode_table):
        return -15, -15
    return 0,memmap(index)
    


def csaveChanges(filename, thread = False):
    if not thread:
        hardWrite(filename)
    else:
        t = threading.Thread(target=hardWrite, args=(filename,))
        t.start() 
    

def cchDir(file_name, current_inode, currentUser):
    status = chDir(file_name, current_inode, currentUser)
    return status

def ccurrentInode(currentUser):
    return ram.user_space[currentUser][0];


def cpartitionInfo():
    info = "\n"

    for key in ram.mbr:
        info = info + str(key) + ": " + str(ram.mbr[key])+"\n"

    return info

def cblockSize():
    return ram.settings["block_size"]

def clogicalSpace():
    return len(ram.inode_table)


# returns free space in units of block size
def cfreeSpace():
    out = freeBlocks()
    return out

def cmasterBlock():
    out = showMasterBlock();
    return out


def cblocksConsumed(filename, currentUser):
    status, blocks = blocksConsumedByFile(filename, ram.user_space[currentUser][0]);
    return status, blocks


