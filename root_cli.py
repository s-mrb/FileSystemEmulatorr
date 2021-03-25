# SHOULD NOT BE ABLE TO CREATE TWO FOLDERS OF SAME NAME



import ram
import dbg
from call import *
import sys 
from bcolors import *
from error import *
from _thread import *
import multiprocessing

def prompt() :
	sys.stdout.write(f'{bcolors.OKCYAN}<root>{bcolors.ENDC} ')
	sys.stdout.flush()

def root_cli():

    currentUser = "root"
    # add inode#0 whenever root_cli starts up
    ram.user_space[currentUser] = [0,[],[]] 

    print(f"\n{bcolors.OKGREEN}MOUNTED SUCCESSFULLY{bcolors.ENDC}")
    print(f"{bcolors.OKCYAN}You have been entered in CLI (enter e to exit CLI){bcolors.ENDC}\n")
    
    while True:
        prompt()
        if ram.changes == ram.changes_threashold:
            p1 = multiprocessing.Process(target=hardWrite, args=("autoSaved_"+ram.current_fileSystem, )) 
            p1.start()
            ram.changes = 0
        # print(ram.user_space)
        # if len(ram.user_space[currentUser][2]) != 0:
            # print(f"{bcolors.WARNING}Thread returned, use command {bcolors.OKCYAN}t show{bcolors.ENDC} to view threads returned data{bcolors.ENDC}")
        command = input()
        command = command.split()
        arg = [000]
        # e to exit
        if command[0] == 'e':
            sys.exit(0)
            break

        if command[0]=="t" and command[1]=="show":
            for data in ram.user_space[currentUser][2]:
                print(data+"\n")
            ram.user_space[currentUser][2] = []
            continue

        # Prints
        if command[0] == "ls":
            l = cls(ram.user_space[currentUser][0]).split("-")
            dir_item = l[0].split()
            non_dir_item = l[1].split()

            for i,item in enumerate(dir_item):
                if (i+1)%8 == 0:
                    print(f'{bcolors.BOLD}{item}{bcolors.ENDC}')
                else:
                    print(f'{bcolors.BOLD}{item}{bcolors.ENDC}',end=' ')

            for i,item in enumerate(non_dir_item):
                if (i+1)%8 == 0:
                    print(f'{bcolors.OKBLUE}{item}{bcolors.ENDC}')
                else:
                    print(f'{bcolors.OKBLUE}{item}{bcolors.ENDC}',end=' ')
            print()
            continue

        # t operation fname arguments
        # Operations can be 0/1/2
        # 0 = read, 1 = write, 2 = truncate
        # arguments are the same as for read, write and truncate
        if command[0] == "t":
            try:
                sub_command = command[1]
                temp = sub_command.split('-')
                sub_command = int(temp[0])
                delay = 0
                if len(temp) == 2:
                    delay = int(temp[1])



            except:
                arguments_not_int()
                continue

            if (sub_command == 0 or sub_command == 1) and len(command) < 5:
                wrong_argument()
                continue

            if sub_command == 2 and len(command) != 4:
                wrong_argument()
                continue

            if sub_command == 0:
                try:
                    start = int(command[3])
                    end = int(command[4])
                except:
                    arguments_not_int()
                    continue
                start_new_thread(trwt, (command[2], sub_command, ram.user_space[currentUser][0], [start, end], currentUser, delay))
                # trwt(command[2], sub_command, ram.user_space[currentUser][0], [start, end], currentUser) 
                continue

            if sub_command == 1:
                try:
                    loc = int(command[3])
                except:
                    arguments_not_int()
                    continue
                text = ' '.join(command[4:])

                start_new_thread(trwt,(command[2], sub_command, ram.user_space[currentUser][0], [loc, text],currentUser, delay))
                # trwt(command[2], sub_command, ram.user_space[currentUser][0], [loc, text],currentUser)
                continue

            if sub_command == 2:
                try:
                    size = int(command[3])
                except:
                    arguments_not_int()
                    continue

                start_new_thread(trwt,(command[2], sub_command, ram.user_space[currentUser][0], [size], currentUser, delay))
                # trwt(command[2], sub_command, ram.user_space[currentUser][0], [size], currentUser)
                continue
            wrong_argument()
            continue

            



        # If file being created is already in directory table then through error
        if command[0] == "make":
            if len(command) != 3:
                wrong_argument();
                continue;

            # if it is anythin other then 0 then it is for file not dir
            dir_flag = False if command[2]!="0" else True
            cmakeFile(ram.user_space[currentUser][0], command[1], dir_flag)
            ram.changes = ram.changes + 1
            continue;

        if command[0] == "delete":
            if len(command) != 2:
                wrong_argument();
                continue
            status = cdelete(command[1], ram.user_space[currentUser][0]);
            if status == -4:
                fname_not_in_dir()
                continue
            ram.changes = ram.changes + 1
            continue

        # Prints
        if command[0] == "data":
            if len(command) != 2:
                wrong_argument()
                continue
            status, data = cshow_data(int(command[1]))
            if status == -15:
                index_out_of_bound()
                continue
            print(data)
            continue;


        if command[0] == "open":
            if len(command) != 3:
                wrong_argument()
                continue;
            mode = 1 if command[2]!="0" else 0
            status = cOpen(command[1], mode, currentUser)

            
            if status == -13:
                file_already_open();
                continue
            if status == -11:
                file_not_found()
                continue
            continue



        if command[0] == "close":
            if len(command) != 2:
                wrong_argument()
                continue
            status = cClose(command[1])
            if status == -12:
                file_not_open()
                continue
            continue

        # Prints
        if command[0] == "read":
            if len(command) != 4:
                wrong_argument()
                continue

            try:
                start = int(command[2])
                end = int(command[3])
            except:
                arguments_not_int()
                continue
            
            status, text = cread(command[1], start, end)
            if status == -12:
                file_not_open();
                continue
            print(text)
            continue


        


        # write filename loc text
        if command[0] == "write":
            if len(command) < 4:
                wrong_argument()
                continue
            
            fname = command[1]
            try:
                loc = int(command[2])
            except:
                arguments_not_int()
                continue
            text = ' '.join(command[3:])

            status = cwrite(fname, loc, text)
            if status == -7:
                free_space_not_found()
                continue
            if status == -8:
                out_of_scope_memory_accessed_in_file()
                continue
            if status == -12:
                file_not_open();
                continue
            ram.changes = ram.changes + 1
            continue


        if command[0] == "truncate":
            if len(command) != 3:
                wrong_argument()
                continue;
            try:
                size = int(command[2])
            except:
                arguments_not_int()
                continue
            status = ctruncate(command[1], size)
            if status == -9:
                trimming_empty_file()
                continue;
            if status == -12:
                file_not_open();
                continue
            ram.changes = ram.changes + 1
            continue


        if command[0] == "move":
            if len(command) != 3:
                wrong_argument()
                continue
            status = cmove(command[1], command[2], ram.user_space[currentUser][0])
            if status == -4:
                fname_not_in_dir();
                continue;
            if status == -5:
                file_not_a_dir();
                continue
            ram.changes = ram.changes + 1
            continue

        # Prints
        if command[0] == "memmap":
            if len(command) != 2:
                wrong_argument()
                continue
            try:
                index = int(command[1])
            except:
                arguments_not_int()
                continue
            
            mem =cmemmap(index)[1].split('\n')
            for l in mem:

                print(l);
            continue

        if command[0] == "chDir":
            if len(command) != 2:
                wrong_argument()
                continue
            status = cchDir(command[1], ram.user_space[currentUser][0], currentUser)
            if status == -5:
                file_not_a_dir()
                continue
            if status == -11:
                file_not_found()
                continue
            continue

        # Prints
        if command[0] == "currentInode":
            print(ccurrentInode(currentUser));
            continue

        # Prints
        if command[0] == "partitionInfo":
            print(cpartitionInfo());
            continue

        # Prints
        if command[0] == "blockSize":
            print(cblockSize())
            continue
        
        # Prints
        if command[0] == "logicalSpace":
            print(clogicalSpace())
            continue

        if command[0] == "freeSpace":
            
            print(f"Unused memeory blocks:\n {cfreeSpace()}\n")
            
            print(f"Note: Block# " + f"{bcolors.OKGREEN}{str(ram.out_scope_block)}{bcolors.ENDC}" + f" is {bcolors.OKCYAN}out of scope flag{bcolors.ENDC} for this hard disk,it can be different for different disks"
                                                    " it means this block number doesn't exist "  
                                                    "it is kept to maintain heap of fixed size,"
                                                    " whenever a block is used a new out scope block# is added")

            continue

        if command[0] =="masterBlock":
            
            print(f"Master block is at start of hard disk and {bcolors.OKGREEN}contain addresses of major block groups{bcolors.ENDC} which are important for starting filesystem.")
            print("Major block groups are:\n"
                f"\n\t-{bcolors.WARNING}Master Boot Record (mbr){bcolors.ENDC}\t\t->\tBoot record for File System, not system"
                f"\n\t-{bcolors.WARNING}Free Blocks (fb){bcolors.ENDC}\t\t\t->\tContain unused block # to maintain a heap."
                f"\n\t-{bcolors.WARNING}Inode Block (ib){bcolors.ENDC}\t\t\t->\tContains Inode Table")
            print()
            print("Block group name with start and end address is given below:")

            print(cmasterBlock())

            continue

        if command[0] == "blocksConsumed":
            if len(command) != 2:
                wrong_argument()
                continue
            status, blocks = cblocksConsumed(command[1], currentUser)

            if status == -11:
                file_not_found()
                continue
            print(blocks)
            continue

        if command[0] == "saveChanges":

            filename = input(f"Please name saved file, {bcolors.WARNING}you can also overwrite existing file{bcolors.ENDC}, don't forget extension .txt\nEnter {bcolors.OKCYAN}-1{bcolors.ENDC} to go back to CLI\n");
            if filename == "-1":
            	print("");
            	continue
            hardWrite(filename)
            print(f"{bcolors.OKGREEN}{bcolors.OKCYAN}{filename}{bcolors.ENDC} has been updated{bcolors.ENDC}\n")

        else:
            wrong_command()
            print("");

        print()



