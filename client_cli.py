import socket
import time
import sys
import traceback

from bcolors import *

host = ""
port = 0

def setup_connection():
    print(f'Provide host IP address (IPv4) and port number, space separated - {bcolors.WARNING}host port{bcolors.ENDC}, {bcolors.WARNING}e{bcolors.ENDC} to exit')
    while True:
        command = input()
        if command == "e":
            sys.exit(0)
        command = command.split()
        try:
            global port
            port = int(command[1])
        except:
            arguments_not_int()
            print("")
            continue
        try:
            global host
            host = command[0]
            sock = connect2server(command[0], port)
            if sock == -21:
                sock_couldnt_open()
                continue
            if sock:
                return sock
            print(f'{bcolors.WARNING}TRY AGAIN!{bcolors.ENDC}')
            continue
        except Exception:
            traceback.print_exc()
            print(f'{bcolors.WARNING}TRY AGAIN!{bcolors.ENDC}')
            continue





def connect2server(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:    	
        #host = "192.169.9.101"
        location = (host, port)
        try:
            sock.connect(location)
            return sock
        except:
            print(f"{bcolors.OKCYAN}Either your IP is already used by some other connection or connection not available.{bcolors.ENDC}\n")
            sock.close()
            exit(0)

    except Exception:
        traceback.print_exc()


def prompt() :
	sys.stdout.write(f'{bcolors.OKCYAN}<{host}@{port}>{bcolors.ENDC} ')
	sys.stdout.flush()




def prepare_request(command):
    size = len(command);
    request = str(size) + "-" + command;
    return request.encode('utf-8')


def make_request(request, sock):
    try:
        sock.send(request)
    except Exception:
        traceback.print_exc()
        exit(0)



def receive_response():
    response = sock.recv(8).decode('utf-8')

    # server sends '' only when server crashed
    if response == '':
        return -69
    # no would be length of message to be received
    no = ""

    # start index of actual data in first string
    start = 0
    for i,ch in enumerate(response):
        if ch!='-':
            no += ch
            continue
        start = i;
        break

    # size (no of chars) of data to receive
    size = int(no)

    # actual data
    response = response[start+1:]
    while len(response) < size:

        # 64 K is max packet size for TCP
        response = response + sock.recv(6400).decode('utf-8')

    return response




from bcolors import *
from error import *




sock = setup_connection()



def repl():

    
    
    while True:

        prompt()
        commandString = input()


        command = commandString.split()
        arg = [000]

        # e to exit
        if command[0] == 'e':
            req = prepare_request(commandString)
            make_request(req, sock)
            res = receive_response()
            break

        if commandString == "t show":
            req = prepare_request(commandString)
            make_request(req, sock)
            res = receive_response()
            print(res)
            continue

        # Prints
        if command[0] == "ls":
        
            """  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ """
            """    GET request, parse it and receive response    """

            req = prepare_request(commandString)
            make_request(req, sock)
            res = receive_response().split("-")
            if res == -69:
                print("Server crashed")
                exit(0)

            dir_item = res[0].split()
            non_dir_item = res[1].split()

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

            """      END OF COMMUNICATION WITH SERVER            """
            """ _______________________________________________  """

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


                """  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ """
                """    GET request, parse it and receive response    """

                req = prepare_request(commandString)
                make_request(req, sock)
                continue

                """      END OF COMMUNICATION WITH SERVER            """
                """ _______________________________________________  """

            if sub_command == 1:
                try:
                    loc = int(command[3])
                except:
                    arguments_not_int()
                    continue
                text = ' '.join(command[4:])


                """  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ """
                """    GET request, parse it and receive response    """

                req = prepare_request(commandString)
                make_request(req, sock)
                
                # no need to receive as nothing sent
                # res = receive_response()

                # print(res)
                continue

                """      END OF COMMUNICATION WITH SERVER            """
                """ _______________________________________________  """




            if sub_command == 2:
                try:
                    size = int(command[3])
                except:
                    arguments_not_int()
                    continue

                """  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ """
                """    GET request, parse it and receive response    """

                req = prepare_request(commandString)
                make_request(req, sock)

                # no need to receive as nothing is sent
                # res = receive_response()

                # print(res)
                continue

                """      END OF COMMUNICATION WITH SERVER            """
                """ _______________________________________________  """


                
            wrong_argument()
            continue

            



        # If file being created is already in directory table then through error
        if command[0] == "make":
            if len(command) != 3:
                wrong_argument();
                continue;

            """  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ """
            """    GET request, parse it and receive response    """

            req = prepare_request(commandString)
            make_request(req, sock)

            # no need to receive as nothing sent
            # res = receive_response()

            # print(res)
            continue

            """      END OF COMMUNICATION WITH SERVER            """
            """ _______________________________________________  """



            

        if command[0] == "delete":
            if len(command) != 2:
                wrong_argument();
                continue

            """  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ """
            """    GET request, parse it and receive response    """

            req = prepare_request(commandString)
            make_request(req, sock)

            status = int(receive_response())
            if status == -4:
                fname_not_in_dir()
                continue
            continue
            

            """      END OF COMMUNICATION WITH SERVER            """
            """ _______________________________________________  """



        # Prints
        if command[0] == "data":
            if len(command) != 2:
                wrong_argument()
                continue


            """  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ """
            """    GET request, parse it and receive response    """

            req = prepare_request(commandString)
            make_request(req, sock)
            res = receive_response()
            status = int(res[0:3])
            if status == -15:
                index_out_of_bound()
                continue
            print(res[3:])
            continue

            """      END OF COMMUNICATION WITH SERVER            """
            """ _______________________________________________  """




        if command[0] == "open":
            if len(command) != 3:
                wrong_argument()
                continue;
            mode = 1 if command[2]!="0" else 0

            """  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ """
            """    GET request, parse it and receive response    """

            req = prepare_request(commandString)
            make_request(req, sock)
            status = int(receive_response())

            if status == -10:
                file_not_a_dir()
                continue
            
            if status == -13:
                file_already_open();
                continue
            if status == -11:
                file_not_found()
                continue
            continue

            """      END OF COMMUNICATION WITH SERVER            """
            """ _______________________________________________  """






        if command[0] == "close":
            if len(command) != 2:
                wrong_argument()
                continue

            """  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ """
            """    GET request, parse it and receive response    """

            req = prepare_request(commandString)
            make_request(req, sock)
            status = int(receive_response())

            if status == -12:
                file_not_open()
                continue
            continue

            """      END OF COMMUNICATION WITH SERVER            """
            """ _______________________________________________  """



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
            
            """  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ """
            """    GET request, parse it and receive response    """

            req = prepare_request(commandString)
            make_request(req, sock)

            # received response will contain first three char for status.
            status_text = receive_response()
            status = int(status_text[0:3])
            text = status_text[3:] 

            if status == -12:
                file_not_open();
                continue
            print(text)
            continue

            """      END OF COMMUNICATION WITH SERVER            """
            """ _______________________________________________  """




        


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


            """  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ """
            """    GET request, parse it and receive response    """

            req = prepare_request(commandString)
            make_request(req, sock)
            status = int(receive_response())

            if status == -7:
                free_space_not_found()
                continue
            if status == -8:
                out_of_scope_memory_accessed_in_file()
                continue
            if status == -12:
                file_not_open();
                continue
            continue

            """      END OF COMMUNICATION WITH SERVER            """
            """ _______________________________________________  """



            


        if command[0] == "truncate":
            if len(command) != 3:
                wrong_argument()
                continue;
            try:
                size = int(command[2])
            except:
                arguments_not_int()
                continue


            """  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ """
            """    GET request, parse it and receive response    """

            req = prepare_request(commandString)
            make_request(req, sock)
            status = int(receive_response())

            if status == -9:
                trimming_empty_file()
                continue;
            if status == -12:
                file_not_open();
                continue
            continue

            """      END OF COMMUNICATION WITH SERVER            """
            """ _______________________________________________  """



            


        if command[0] == "move":
            if len(command) != 3:
                wrong_argument()
                continue


            """  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ """
            """    GET request, parse it and receive response    """

            req = prepare_request(commandString)
            make_request(req, sock)
            status = int(receive_response())

            
            if status == -4:
                fname_not_in_dir();
                continue;
            if status == -5:
                file_not_a_dir();
                continue
            continue

            """      END OF COMMUNICATION WITH SERVER            """
            """ _______________________________________________  """



            

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


            """  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ """
            """    GET request, parse it and receive response    """

            req = prepare_request(commandString)
            make_request(req, sock)
            res = receive_response()
            status = int(res[0:3])
            if status == -15:
                index_out_of_bound()
                continue
            print(res[3:])
            mem = res[3:][1].split('\n')
            for l in mem:
                print(l)
            continue


            """      END OF COMMUNICATION WITH SERVER            """
            """ _______________________________________________  """


            

        if command[0] == "chDir":
            if len(command) != 2:
                wrong_argument()
                continue


            """  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ """
            """    GET request, parse it and receive response    """

            req = prepare_request(commandString)
            make_request(req, sock)
            status = int(receive_response())
            
            if status == -5:
                file_not_a_dir()
                continue
            if status == -11:
                file_not_found()
                continue
            continue

            """      END OF COMMUNICATION WITH SERVER            """
            """ _______________________________________________  """



            

        # Prints
        if command[0] == "currentInode":

            """  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ """
            """    GET request, parse it and receive response    """

            req = prepare_request(commandString)
            make_request(req, sock)
            res = receive_response()

            print(res)
            continue

            """      END OF COMMUNICATION WITH SERVER            """
            """ _______________________________________________  """


            

        # Prints
        if command[0] == "partitionInfo":

            """  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ """
            """    GET request, parse it and receive response    """

            req = prepare_request(commandString)
            make_request(req, sock)
            res = receive_response()

            print(res)
            continue

            """      END OF COMMUNICATION WITH SERVER            """
            """ _______________________________________________  """

            

        # Prints
        if command[0] == "blockSize":

            """  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ """
            """    GET request, parse it and receive response    """

            req = prepare_request(commandString)
            make_request(req, sock)
            res = receive_response()

            print(res)
            continue

            """      END OF COMMUNICATION WITH SERVER            """
            """ _______________________________________________  """

            
        
        # Prints
        if command[0] == "logicalSpace":

            """  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ """
            """    GET request, parse it and receive response    """

            req = prepare_request(commandString)
            make_request(req, sock)
            res = receive_response()

            print(res)
            continue

            """      END OF COMMUNICATION WITH SERVER            """
            """ _______________________________________________  """

            

        if command[0] == "freeSpace":

            """  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ """
            """    GET request, parse it and receive response    """

            req = prepare_request(commandString)
            make_request(req, sock)

            # out_scope_block freeSpace
            res = receive_response().split()


            """      END OF COMMUNICATION WITH SERVER            """
            """ _______________________________________________  """


            out_scope_block = res[0]
            free_space = res[1]
            print(f"Unused memeory blocks:\n {free_space}\n")
            
            print(f"Note: Block# " + f"{bcolors.OKGREEN}{str(out_scope_block)}{bcolors.ENDC}" + f" is {bcolors.OKCYAN}out of scope flag{bcolors.ENDC} for this hard disk,it can be different for different disks"
                                                    " it means this block number doesn't exist "  
                                                    "it is kept to maintain heap of fixed size,"
                                                    " whenever a block is used a new out scope block# is added")
            print("")
            continue

        if command[0] =="masterBlock":

            """  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ """
            """    GET request, parse it and receive response    """

            req = prepare_request(commandString)
            make_request(req, sock)

            # res is masterblock info
            res = receive_response()


            """      END OF COMMUNICATION WITH SERVER            """
            """ _______________________________________________  """


            print(f"\nMaster block is at start of hard disk and {bcolors.OKGREEN}contain addresses of major block groups{bcolors.ENDC} which are important for starting filesystem.")
            print("Major block groups are:\n"
                f"\n\t-{bcolors.WARNING}Master Boot Record (mbr){bcolors.ENDC}\t\t->\tBoot record for File System, not system"
                f"\n\t-{bcolors.WARNING}Free Blocks (fb){bcolors.ENDC}\t\t\t->\tContain unused block # to maintain a heap."
                f"\n\t-{bcolors.WARNING}Inode Block (ib){bcolors.ENDC}\t\t\t->\tContains Inode Table")
            print()
            print("Block group name with start and end address is given below:")

            print(res)

            continue

        if command[0] == "blocksConsumed":
            if len(command) != 2:
                wrong_argument()
                continue

            """  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ """
            """    GET request, parse it and receive response    """

            req = prepare_request(commandString)
            make_request(req, sock)

            # status + data
            res = receive_response()
            status = int(res[0:3])
            blocks = res[3:]
            

            """      END OF COMMUNICATION WITH SERVER            """
            """ _______________________________________________  """


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
            req = prepare_request(f"saveChanges {filename}")
            make_request(req, sock)
            print(f"{bcolors.OKGREEN}{bcolors.OKCYAN}{filename}{bcolors.ENDC} has been updated{bcolors.ENDC}\n")


        else:
            wrong_command()
            print("");

        print()



try:

    repl()
except Exception:
    traceback.print_exc()
    exit(0)
