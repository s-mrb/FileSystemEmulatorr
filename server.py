import socket
from _thread import *
import threading
import pickle
from bcolors import *
from request_handler import processRequest
from error import *
import multiprocessing
from hard_write import hardWrite
# bht ganda kam, allowing server thread to access one variable from ram
import ram



# from root_cli import root_cli
huge_file = "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"
# from repl2 import *


import traceback





def make_socket():
    ssocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    return ssocket

def start_listening(port = 55555, ssocket = None, clients = 3):
    # host = socket.gethostname()
    host = ''
    ssocket.bind((host, port))
    ssocket.listen(clients)
    print(f"Listeing on port {port}")



def prepare_response(response):
    size = len(response);
    msg = str(size) + "-" + response;
    return msg.encode('utf-8')

def make_response(response, connection):
    connection.send(response)



def receive_request(connection):
    request = connection.recv(8).decode('utf-8')

    # no would be length of message to be received
    no = ""

    # start index of actual data in first string
    start = 0
    for i,ch in enumerate(request):
        if ch!='-':
            no += ch
            continue
        start = i;
        break

    # size (no of chars) of data to receive
    size = int(no)

    # actual data
    command = request[start+1:]
    while len(command) < size:

        # 64 K is max packet size for TCP
        command = command + connection.recv(6400).decode('utf-8')

    return command






def handle_client(connection, currentUser, mode):
    while True:
        if ram.changes == ram.changes_threashold:
            p1 = multiprocessing.Process(target=hardWrite, args=("autoSaved"+ram.current_fileSystem, )) 
            p1.start()
            ram.changes = 0
        command = receive_request(connection)

        # If client sends -1 then close that clients connection.
        if command == "e":

            # remove userSpace first
            stat = processRequest(command, currentUser)

            # send ok
            make_response("0-".encode('utf-8'), connection)

            


            # then close connection
            connection.close()

            if mode == 0:
                print(f'{bcolors.WARNING}Connection with user {currentUser}  is closed.{bcolors.ENDC}')

            # then close thread
            return
            

        # response to be sent to client
        msg = processRequest(command, currentUser)
        if msg == "0":
            continue

        size = len(msg)
        msg = str(size) + "-" + msg;
        connection.send((msg.encode('utf-8')))

    connection.close()



def server_thread(ssocket, mode):
    while True:
        connection, address = ssocket.accept()
        if address[0] in ram.user_space:
            connection.close();
            continue;

        currentUser = address[0]

        # in user space of user save current inode #
        # in the start this is just 0
        # userspace = [inode#, array of parent stack, array of threads_output
        ram.user_space[currentUser] = [0,[],[]]

        # if it is server mode then show prompt regarding new connections
        # else keep an array for of connections
        if mode == 0:
            print(f'{bcolors.WARNING}Connected to: {address[0]} on port {str(address[1])}{bcolors.ENDC}')
        start_new_thread(handle_client, (connection,currentUser, mode))
    ssocket.close()


def setup_server():
    print(f'Provide port number and client limmit, space separated - {bcolors.WARNING}port clients{bcolors.ENDC}')
    while True:
        port_client = input().split()
        if len(port_client) != 2:
            wrong_argument()
            continue
        try:
            port = int(port_client[0])
            clients_allowed = int(port_client[1])
        except:
            arguments_not_int()
            continue
        try:
            ssocket = make_socket();
            start_listening(port=port,ssocket=ssocket, clients = clients_allowed);
            return ssocket;
        except Exception as e:
            traceback.print_exc()
            print(f'{bcolors.WARNING}WRITE AGAIN!{bcolors.ENDC}')
            continue
