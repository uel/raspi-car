import requests
import time


def Up():
    pass

def Down():
    pass

def Left():
    pass

def Right():
    pass

def RequestCommands():
    #requests.get()
    pass

def ExecuteCommand(command):
    pass

lastCommandTime = 1000
while True:
    commands = RequestCommands()
    
    if commands != []:
        lastCommandTime = time.time()
        for command in commands:
            ExecuteCommand()
            commands = []

    if time.time()-lastCommandTime < 2:
        time.sleep(0.05)
    else:
        time.sleep(3)


