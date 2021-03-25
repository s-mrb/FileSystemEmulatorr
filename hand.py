
import ram
import dbg

from mount import start
from create import makeFile
from move import move
from delete import deleteFile
from ls import ls
from chDir import chDir
from dir_table import get_dir_table

from OpenFile import Open
from hard_write import hardWrite
from call import *


"""

SHOW PARENT 


make dictionary of errors where key is status and value is correspong error function, 
on key = 0, print second string, else call error 


Change ls to return string
                            send status and
                            ls should return a string where each item is space separated
                            and directories and files are - separated

Change freeBlocks       
                            send status and
                            send - blocks left and out_if scope block

Change Master block
                            send status, master block string
do everything 

USE ram.current_inode to create the illusion for each user being in separate directory simultaneously

"""
start()


cmakeFile(ram.current_inode, "f1", 0)


# print(showMasterBlock())
# print(freeBlocks())
# a = cls(ram.current_inode)
# a = a.split('-')
# print(a)
# exit(0)
# cOpen("f1", 0)
cwrite("f1","aha wow cool", 0)
# print(cread("f1", 0, -1))
# cls(ram.current_inode, True)
# print(cmemmap())
# csaveChanges("xx2",True)
# print(blocksConsumed("f1"))
# print(cshow_data())
# print(cshow_data())
# cdelete("f1", ram.current_inode)
# cls(ram.current_inode)
# ram.oft["f1"].write("abcdefg",0)



# trwt( "f1", 0, ram.current_inode,[0, -1] )

def r():
    trwt( "f1", 1, ram.current_inode,[0, "o fuck my life g"] )

r();
print("aha")
# trwt( "f1", 1, ram.current_inode,[0, "o fuck my life g"] )
# trwt( "f1", 0, ram.current_inode,[0, -1] )
# trwt( "f1", 2, ram.current_inode,[6] )
# trwt( "f1", 0, ram.current_inode,[0, -1] )
exit()
# trwt( "f1", 1, [0, "Ok fuck me=y life"] )

# trwt( "f1", 2, [6] )
# trwt( "f1", 0, [0, -1] )
# trwt( fname, method, arguments )



# print(ram.oft["f1"].read(0,-1))
exit(0)

# ls(ram.current_inode)

# openedFile = cOpen("f1", thread = True);

# openedFile.write("abc",0)




# makeFile(ram.current_inode, "f1", 0)
# openedFile = Open("f1");

# openedFile.write("abc",0)
# # openedFile.truncate(2)
# text = openedFile.read(0,4)
# print(type(ram.inode_table[0][9][0]))
# hardWrite("newt")
# print(type(ram.inode_table[0][9][0]))
# makeFile(ram.current_inode, "f1", 0)
# ls(ram.current_inode)

# exit(0)
# # makeFile(ram.current_inode, "f3", 0)
# ls(ram.current_inode)
# print(text)
# exit(0)

# # makeFile(ram.current_inode, "f2")

# from mount import  out_scope_block


# print(ram.current_inode)
# ls(ram.current_inode)
# for inode in ram.inode_table:
#     print(inode)
# for data in dbg.data:
#     print(data)

# # print(ram.parents_stack)
# # print(ram.current_inode);
# chDir("f1",ram.current_inode);
# print(ram.current_inode)
# ls(ram.current_inode)
# for inode in ram.inode_table:
#     print(inode)
# for data in dbg.data:
#     print(data)
# exit(0)

# makeFile(ram.current_inode, "f1")
# print(ram.parents_stack)
# print(ram.current_inode);



# print(ram.parents_stack)
# print(ram.current_inode);
# chDir("..",ram.current_inode);
# makeFile(ram.current_inode, "f1")
# print(ram.parents_stack)
# print(ram.current_inode);

# print(ram.free_blocks)
# for inode in ram.inode_table:
#     print(inode)
# for data in dbg.data:
#     print(data)

# print("")
# move("f1","f2", ram.current_inode)

# print(ram.free_blocks)
# for inode in ram.inode_table:
#     print(inode)
# for data in dbg.data:
#     print(data)


# deleteFile("f2",ram.current_inode)


# for inode in ram.inode_table:
#     print(inode)
# for data in dbg.data:
#     print(data)
