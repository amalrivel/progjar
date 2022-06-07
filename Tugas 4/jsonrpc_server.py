#!/usr/bin/env python3
# Foundations of Python Network Programming, Third Edition
# https://github.com/brandon-rhodes/fopnp/blob/m/py3/chapter18/jsonrpc_server.py
# JSON-RPC server needing "pip install jsonrpclib-pelix"

from http import server
from re import S
from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer
import argparse, socket
import sys
import glob
import pathlib
import os
import time




def lengths(*args):
    """Measure the length of each input argument.

    Given N arguments, this function returns a list of N smaller
    lists of the form [len(arg), arg] that each state the length of
    an input argument and also echo back the argument itself.

    """
    results = []
    for arg in args:
        try:
            arglen = len(arg)
        except TypeError:
            arglen = None
        results.append((arglen, arg))
    # return arg
    second_text = arg.split()
    if second_text[0] == "ping":
        remove_ping = second_text[1:]
        join_now = ' '.join(remove_ping)
        # print('  Textnya :', repr(join_now))
        # print('  Message len:', repr(len(join_now)))
        return join_now

    if second_text[0] == "exit":
        # print('Server shutdown...') 
        # time.sleep(2)
        # print('Client shutdown...') 
        # server.shutdown()
        return arg

        
    if second_text[0] == "get":
        path_file = second_text[1]
        path=second_text[1]
        name_file = second_text[2]
        helper = "/"
        space = " "
        path_file=path_file+helper+name_file

        f=open(path_file,"rb")
        b=f.read()
        length = len(b)

        # print('Fetch:',path) 
        # print('size :',length)
        # print('lokal :',name_file)
        new_length = b"%03d" % (len(b),) 
        output = path.encode() + space.encode() + new_length + space.encode() + name_file.encode() 
        argu = output.decode()
        # len_output = b"%03d" % (len(output.decode()),) 
        return argu

    if second_text[0] == "ls":
        # path = "*.py"
        # for file in glob.glob(path, recursive=True):
        #     print(file)
        # if len(second_text) == 1:
        #     dest = '*.py'
        if len(second_text) == 1:
            dest = '*.py'

        if len(second_text) == 2:
            dest = second_text[1]
        # if second_text[1] != "":
        #     dest = second_text[1]
        list_file =  glob.glob(dest)
        space = ''
        for i in list_file:
            space += i + '\n'

        # print('Output:')
        # print(space)
        return space

    if second_text[0] == "count":
        # path = "*.py"
        # for file in glob.glob(path, recursive=True):
        #     print(file)
        # if len(second_text) == 1:
        #     dest = '*.py'
        if len(second_text) == 1:
            dest = '*.py'

        if len(second_text) == 2:
            dest = second_text[1]
        # if second_text[1] != "":
        #     dest = second_text[1]
        list_file =  glob.glob(dest)
        space = ''
        for i in list_file:
            space += i + '\n'

        count =  len(list_file)
        # print('Output:')
        # print(space)
        return count


def main():
    server = SimpleJSONRPCServer(('localhost', 7002))
    server.register_function(lengths)
    print("Starting server")
    server.serve_forever()

if __name__ == '__main__':
    main()
