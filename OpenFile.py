import ram
import dbg

import math
from dir_table import get_dir_table
block_size = ram.settings["block_size"]

class OpenFile:
    def __init__(self,fname,mode, parent_inode, file_inode):
        self.parent_inode = parent_inode;
        self.inode = file_inode
        self.mode = mode;
        self.name = fname

    def __repr__(self):
        return str(id(self))

    def read(self,start=0, end=-1):
        global block_size
        if ram.inode_table[self.inode][9][0]==-1:
            return "";
        # get block_no for start
        start_block_no = math.floor(start / block_size);
        end_block_no = end if end == -1 else math.floor(start / block_size);

        loc1 = start
        displacement4start = 0
        while (loc1 % block_size) != 0:
            displacement4start = displacement4start + 1;
            loc1 = loc1 - 1

        displacement4end = -1
        if end_block_no != -1:
            loc1 = end
            displacement4end = 0
            while (loc1 % block_size) != 0:
                displacement4end = displacement4end + 1;
                loc1 = loc1 - 1

        # get addr_list
        address_list = ram.inode_table[self.inode][9]
        #
        # print(end_block_no)
        # print(start_block_no)
        if end_block_no - start_block_no == 0:
            # print(data[address_list[start_block_no]][displacement4start:end + 1])
            return dbg.data[address_list[start_block_no]][displacement4start:end + 1]
        first_chunk = dbg.data[address_list[start_block_no]][displacement4start:]
        last_chunk = dbg.data[address_list[end_block_no]][:displacement4end + 1]

        # find mid chunk

        address_list = address_list[start_block_no:end_block_no + 1] if end_block_no != -1 else address_list[
                                                                                                start_block_no:]
        address_list.pop(0);
        if len(address_list) == 0:
            # print(first_chunk + last_chunk);
            return first_chunk + last_chunk
        address_list.pop(-1);

        if len(address_list) == 0:
            # print(first_chunk + last_chunk);
            return first_chunk + last_chunk

        mid_chunk = ""
        for i in range(len(address_list)):
            mid_chunk = mid_chunk + dbg.data[address_list[i]]

        # print(mid_chunk)
        return mid_chunk

    def close(self):
        return False

    def write(self,loc=0, text ="Hi"):
        global block_size
        if ram.inode_table[self.inode][9][0] == -1:
            chars_left = len(text)
            required_blocks = math.ceil(chars_left / block_size)
            blocks = []

            # see how many blocks will be required for this data
            for i in range(required_blocks):
                new_addrs = ram.free_blocks.pop(0)
                blocks.extend([new_addrs])
                if new_addrs == ram.out_scope_block:
                    return -7

                ram.free_blocks.extend([ram.out_scope_block])

            # update addr_list for this inode
            ram.inode_table[self.inode][9] = blocks

            # fill all newly created blocks
            for i in range(len(blocks)):
                if len(text) - block_size > 0:

                    # data[blocks[i]] is list item not string
                    dbg.data[blocks[i]] = text[0:block_size]
                    text = text[block_size:]
                else:
                    if len(dbg.data) == blocks[i]:
                        dbg.data.append(text)
                    else:
                        dbg.data[blocks[i]] = text
        else:
            # find block number

            block_no = math.floor(loc / block_size);

            # find displacement within the block
            loc2 = loc
            displacement = 0
            while (loc2 % block_size) != 0:
                displacement = displacement + 1;
                loc2 = loc2 - 1

            block_addr_list = ram.inode_table[self.inode][9]

            total_posible_chars_in_all_lists = len(block_addr_list) * block_size;
            if loc > (total_posible_chars_in_all_lists) - 1:
                # out_of_scope_memory_accessed_in_file()
                return -8

            block_addr_list = block_addr_list[block_no:]
            while (len(text) != 0 and len(block_addr_list) != 0):
                addr = block_addr_list.pop(0)

                # ? DON't KNOW
                # print("aaaaaaaa"+str(inode_table[opened.inode][9]))
                # inode_table[opened.inode][9].extend([addr]);
                # print("aaaaaaaa" + str(inode_table[opened.inode][9]))
                if loc == 0 or loc % block_size == 0:
                    if len(text) - block_size > 0:
                        dbg.data[addr] = text[0:block_size]
                        text = text[block_size:]
                    else:
                        copied = dbg.data[addr][len(text):0]
                        dbg.data[addr] = text + copied
                        return 0
                else:
                    copied = dbg.data[addr][0:loc]
                    index2 = None if len(text) < block_size - len(copied) else block_size - displacement + 1

                    if index2:
                        text2append = text[0:index2];
                        text = text[index2:]
                        new_data = copied + text2append
                        dbg.data[addr] = new_data
                    else:
                        text2append = text
                        start_block = copied + text2append
                        end_block = dbg.data[addr][len(start_block):]
                        new_data = start_block + end_block;
                        dbg.data[addr] = new_data;
                        text = ""
            # print("aaaaaaaa" + str(inode_table[opened.inode][9]))
            chars_left = len(text)
            required_blocks = math.ceil(chars_left / block_size)
            blocks = []

            # see how many blocks will be required for this data
            for i in range(required_blocks):
                new_addrs = ram.free_blocks.pop(0)
                blocks.extend([new_addrs])
                if new_addrs == ram.out_scope_block:
                    return -7
                ram.free_blocks.extend([ram.out_scope_block])

            # update addr_list for this inode
            ram.inode_table[self.inode][9].extend(blocks)

            # fill all newly created blocks
            for i in range(len(blocks)):
                if len(text) - block_size > 0:

                    # data[blocks[i]] is list item not string
                    dbg.data[blocks[i]] = text[0:block_size]
                    text = text[block_size:]
                else:
                    if len(dbg.data) == blocks[i]:
                        dbg.data.append(text)
                    else:
                        dbg.data[blocks[i]] = text
            return 0
        return 0

    def truncate(self, size):
        global block_size
        if size == 0:
            return 0
        addr_list = ram.inode_table[self.inode][9]
        if addr_list[0] == -1:
            # trimming_empty_file()
            return -9


        if size < block_size:
            addr = addr_list[-1]
            data_len = len(dbg.data[addr]);
            if size >= data_len:
                ram.inode_table[self.inode][9].pop(-1);
                if len(ram.inode_table[self.inode][9]) == 0:
                    ram.inode_table[self.inode][9] = [-1]
                dbg.data[addr] = "deleted";
                size = size - data_len
            else:
                new_data = dbg.data[addr][0:data_len - size];
                dbg.data[addr] = new_data;

            if size > 0:
                new_data = dbg.data[addr][0:data_len - size];
                dbg.data[addr] = new_data;
                return 0
        else:
            addr = ram.inode_table[self.inode][9].pop(-1);
            if len(ram.inode_table[self.inode][9]) == 0:
                ram.inode_table[self.inode][9] = [-1]
            dbg.data[addr] = "deleted";
            size = size - block_size;
            self.truncate(size)

    def move(self):
        pass

def Open(fname, current_inode):
    current_dir_table = get_dir_table(current_inode)

    if fname not in current_dir_table:
        return -11, -11
    file_inode = current_dir_table[fname]
    if ram.inode_table[file_inode][1] == 0:
        return -10, -10

    return 0,OpenFile(fname=fname, mode="this para is no longer needed here", parent_inode=current_inode, file_inode=file_inode)

# def Close(opened_filename):
#     repr(opened_filename)
#     opened_filename = None
#
# # opened = Open("public","a")
# #
# # Close(opened)
# # opened = None
# # print(opened)
