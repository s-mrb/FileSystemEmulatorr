# Root user can decide port, run server, shut down server, decide filesystem to mount
from server import *
from root_cli import root_cli
from mount import mount
from bcolors import *
from error import *
import sys







def mode_server(ssocket):
    # mode == 0 if only server mode else 1
    server_thread(ssocket, mode = 0);

def mode_root():
    root_cli()

def mode_dual(ssocket):
    server_backend = threading.Thread(target = server_thread,args=(ssocket,1));
    root_backend_cli = threading.Thread(target = root_cli,args=());
    server_backend.start()
    root_backend_cli.start()
    server_backend.join()
    root_backend_cli.join()




def run_mode():
    print(f'\nAvailable commands\n\n\t{bcolors.OKCYAN}mode server{bcolors.ENDC}\n\t{bcolors.OKCYAN}mode root{bcolors.ENDC}\n\
    \t{bcolors.OKCYAN}mode dual{bcolors.ENDC}\n\t{bcolors.OKCYAN}exit{bcolors.ENDC}\n')


    prompt_flag = 0
    while not prompt_flag:
        command = input()
        if command == "mode server":
            prompt_flag = 1
            ssocket = setup_server();
            mode_server(ssocket)
        if command == "mode root":
            prompt_flag == 1
            mode_root()
        if command == "mode dual":
            prompt_flag == 1
            ssocket = setup_server();
            mode_dual(ssocket)
        if command == "exit":
            sys.exit(0)
        else:
            wrong_command()
            print("")
            continue




