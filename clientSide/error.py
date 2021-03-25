from bcolors import *

# status = -1
def fs_corrupted():
            print(f"{bcolors.FAIL}Error: Your file system is corrupted or not found!!"
                  f"\nRe-initialize your system by running initialize_fs.py{bcolors.ENDC}")
            exit(0)


# status = -2
def wrong_argument():
    print(f"{bcolors.FAIL}Error: Please check your arguments!!{bcolors.ENDC}")
    return


# status = -3
def wrong_command():
    print(f"{bcolors.FAIL}Error: Command not found!!{bcolors.ENDC}")
    return


# status = -4
def fname_not_in_dir():
    print(f"{bcolors.FAIL}Error: File name is not present in current directory!!{bcolors.ENDC}")
    return


# status = -5
def file_not_a_dir():
    print(f"{bcolors.FAIL}Error: File not a directory!!!!{bcolors.ENDC}")



# status = -6
def disks_error():
    print(f"{bcolors.FAIL}Error: Number of disks can not be greater than total inode entries!!{bcolors.ENDC}")



# status = -7
def free_space_not_found():
    print(f"{bcolors.FAIL}Error: Entire disk is used up and no free space is found for new entry!!{bcolors.ENDC}")


# status = -8
def out_of_scope_memory_accessed_in_file():
    print(f"{bcolors.FAIL}Error: Location accessed is not present within this file!!{bcolors.ENDC}")



# status = -9
def trimming_empty_file():
    print(f"{bcolors.FAIL}Error: You can not trim empty file!!{bcolors.ENDC}")



# status = -10
def operation_not_for_folders():
    print(f"{bcolors.FAIL}Error: This operation can not be performed on folders/directories!!{bcolors.ENDC}")




# status = -11
def file_not_found():
    print(f"{bcolors.FAIL}Error: Specified file or directory not found!!{bcolors.ENDC}")


# status = -12
def file_not_open():
    print(f"{bcolors.FAIL}Error: Specified file not found in open file table!!{bcolors.ENDC}")

# status = -13
def file_already_open():
    print(f"{bcolors.FAIL}Error: Specified file is already present in open file table!!{bcolors.ENDC}")

# status = -14
def arguments_not_int():
    print(f"{bcolors.FAIL}Error: Integer arguemnts were required but string given!!{bcolors.ENDC}")


# status = -15
def index_out_of_bound():
    print(f"{bcolors.FAIL}Error: Index out of bound!!{bcolors.ENDC}")

    