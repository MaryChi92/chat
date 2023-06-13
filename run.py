from subprocess import Popen, CREATE_NEW_CONSOLE

NUMBER_OF_CLIENTS_LISTEN = 3
NUMBER_OF_CLIENTS_SEND = 2
process_list = []

while True:
    action = input("Start server and clients (s) / Close all clients (x) / Quit (q) ")

    if action == 's':
        process_list.append(Popen('python server.py', creationflags=CREATE_NEW_CONSOLE))
        for i in range(NUMBER_OF_CLIENTS_LISTEN):
            process_list.append(Popen('python client.py "localhost" 7777 -m listen', creationflags=CREATE_NEW_CONSOLE))
        for i in range(NUMBER_OF_CLIENTS_SEND):
            process_list.append(Popen('python client.py "localhost" 7777 -m send', creationflags=CREATE_NEW_CONSOLE))
    elif action == 'x':
        for p in process_list:
            p.kill()
        process_list.clear()
    else:
        break
