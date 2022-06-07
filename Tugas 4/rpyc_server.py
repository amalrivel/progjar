#!/usr/bin/env python3
# Foundations of Python Network Programming, Third Edition
# https://github.com/brandon-rhodes/fopnp/blob/m/py3/chapter18/rpyc_server.py
# RPyC server


import rpyc
import sys
import glob
import os

def main():
    from rpyc.utils.server import ThreadedServer
    t = ThreadedServer(MyService, port = 18861)
    t.start()

class MyService(rpyc.Service):
    def exposed_exeCommand(self, text):
        commands = text.split()
        if commands[0] == "ping":
            remove_ping = commands[1:]
            join_now = ' '.join(remove_ping) + '\n'
            return join_now

        elif commands[0] == "ls":
            if len(commands) == 1:
                mainPath = '*'
            else:
                mainPath = commands[1]
            files = glob.glob(mainPath, recursive=True)
            basenames = ""
            for file in files:
                basenames += os.path.basename(file) + '\n'
            return basenames

        elif commands[0] == "count":
            if len(commands) == 1:
                mainPath = '*'
            else:
                mainPath = commands[1]

            files = glob.glob(mainPath)
            count = len(files)
            return count
        
        elif commands[0] == "get":
            path = commands[1]
            file_name = commands[2]
            size = 0

            for files in os.scandir(path):
                basename = os.path.basename(files)
                if basename == file_name:
                    f = open(files,"rb")
                    reader = f.read()
                    size += len(reader)
                    f.close()
            
            getFile = "fetch: " + path + " size: " + str(size) + " lokal: " + file_name
            return getFile

        elif commands[0] == "put":
            location = ' '.join(commands[2:])
            filenames = str(commands[1])
            fullLocation = os.path.join(location,filenames)
            path = str(fullLocation)
            f=open(path, "w+")
            f.close()
            messages = "put: " + filenames + " lokal: " + path
            return messages

        elif commands[0] == "quit":
            sys.exit(0)
            
if __name__ == '__main__':
    main()