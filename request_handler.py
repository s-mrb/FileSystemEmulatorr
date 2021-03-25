# SHOULD NOT BE ABLE TO CREATE TWO FOLDERS OF SAME NAME



import ram
import dbg
# from mount import start
from call import *
from _thread import *

from bcolors import *
from error import *


def processRequest(command, currentUser):
    
    command = command.split()
    arg = [000]
    
    if command[0] == "e":
        ram.user_space.pop(currentUser)
        

    if command[0]=="t" and command[1]=="show":

        res = "  "
        print("In t show")
        for data in ram.user_space[currentUser][2]:
            res = res + data+"\n"

        ram.user_space[currentUser][2] = []
        return res

    # Prints
    if command[0] == "ls":
        return cls(ram.user_space[currentUser][0])

    # t operation fname arguments
    # Operations can be 0/1/2
    # 0 = read, 1 = write, 2 = truncate
    # arguments are the same as for read, write and truncate
    if command[0] == "t":

        sub_command = command[1]
        temp = sub_command.split('-')
        sub_command = int(temp[0])
        delay = 0
        if len(temp) == 2:
            delay = int(temp[1])

        if sub_command == 0:
            start = int(command[3])
            end = int(command[4])

            # for truly multithreaded client-server communication this must not be returned here
            start_new_thread(trwt,(command[2], sub_command, ram.user_space[currentUser][0], [start, end], currentUser, delay))
            # trwt(command[2], sub_command, ram.user_space[currentUser][0], [start, end], currentUser)
            return "0" 

        if sub_command == 1:
            loc = int(command[3])            
            text = ' '.join(command[4:])
            
            # for truly multithreaded client-server communication this must not be returned here
            start_new_thread(trwt,(command[2], sub_command, ram.user_space[currentUser][0], [loc, text], currentUser, delay))
            # trwt(command[2], sub_command, ram.user_space[currentUser][0], [loc, text], currentUser)
            
            return "0"

        if sub_command == 2:
            
            size = int(command[3])

            # for truly multithreaded client-server communication this must not be returned here
            start_new_thread(trwt,(command[2], sub_command, ram.user_space[currentUser][0], [size], currentUser, delay))
            # trwt(command[2], sub_command, ram.user_space[currentUser][0], [size], currentUser)
            return "0"    
        

        



    # If file being created is already in directory table then through error
    if command[0] == "make":

        # if it is anythin other then 0 then it is for file not dir
        dir_flag = False if command[2]!="0" else True
        cmakeFile(ram.user_space[currentUser][0], command[1], dir_flag)
        ram.changes = ram.changes + 1
        return "0";

    if command[0] == "delete":

        status = cdelete(command[1], ram.user_space[currentUser][0]);
        ram.changes = ram.changes + 1
        return str(status)

    # Prints
    if command[0] == "data":
        status, data = cshow_data(int(command[1]))
        if status < 0:
            return str(status)
        return "100"+data


    if command[0] == "open":

        mode = 1 if command[2]!="0" else 0
        status = cOpen(command[1], mode, currentUser)
        if status == 0:
            return "100"
        return str(status)



    if command[0] == "close":

        status = cClose(command[1])
        if status == 0:
            return "100"
        return str(status)

    # Prints
    if command[0] == "read":

        start = int(command[2])
        end = int(command[3])

        status, text = cread(command[1], start, end)
        if status == 0:
            status = "100"
        return str(status) + str(text)





    # write filename loc text
    if command[0] == "write":

        fname = command[1]
        loc = int(command[2])

        text = ' '.join(command[3:])

        status = cwrite(fname, loc, text)

        if status == 0:
            return "100"
        ram.changes = ram.changes + 1
        return str(status)


    if command[0] == "truncate":

        size = int(command[2])

        status = ctruncate(command[1], size)
        if status == 0:
            return "100"
        ram.changes = ram.changes + 1
        return str(status)


    if command[0] == "move":

        status = cmove(command[1], command[2], ram.user_space[currentUser][0])
        if status == 0:
            return "100"
        ram.changes = ram.changes + 1
        return str(status)

    # Prints
    if command[0] == "memmap":
        index = int(command[1])
        status, map = cmemmap(index)
        if status == -15:
            return str(status)
        return "100"+map

    if command[0] == "chDir":

        status = cchDir(command[1], ram.user_space[currentUser][0],currentUser)
        if status == 0:
            return "100"
        return str(status)

    # Prints
    if command[0] == "currentInode":
        cinode = ccurrentInode(currentUser);

        # 0 is used as flag to not respond to client,so make it 00
        if cinode == 0:
            return "00"
        return str(cinode);

    # Prints
    if command[0] == "partitionInfo":
        return cpartitionInfo();


    # Prints
    if command[0] == "blockSize":
        return str(cblockSize())
    
    # Prints
    if command[0] == "logicalSpace":
        return str(clogicalSpace())

    if command[0] == "freeSpace":
        return str(ram.out_scope_block) +" "+ str(cfreeSpace())


    if command[0] =="masterBlock":
        return cmasterBlock()


    if command[0] == "blocksConsumed":

        status, blocks = cblocksConsumed(command[1],currentUser)
        if status == 0:
            status = "100"
    
        elif status < 0:
            return str(status)
        return str(status) + ' '.join([str(x) for x in blocks])


    if command[0] == "saveChanges":

        hardWrite(filename)
        return 0


