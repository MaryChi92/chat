from subprocess import Popen, CREATE_NEW_CONSOLE

process_list = []

while True:
    action = input("Start server and clients (enter number of clients) / Close all clients (x) / Quit (q) ")

    if action.isdigit():
        process_list.append(Popen('python server.py', creationflags=CREATE_NEW_CONSOLE))
        for i in range(int(action)):
            process_list.append(Popen('python client.py "localhost" 7777', creationflags=CREATE_NEW_CONSOLE))
    elif action == 'x':
        for p in process_list:
            p.kill()
        process_list.clear()
    else:
        break
