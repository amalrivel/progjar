#!/usr/bin/env python3
# Foundations of Python Network Programming, Third Edition
# https://github.com/brandon-rhodes/fopnp/blob/m/py3/chapter18/rpyc_client.py
# RPyC client

import rpyc, sys

def main():
    while True:
        config = {'allow_public_attrs': True}
        proxy = rpyc.connect('localhost', 18861, config=config)
        print("Input Client: ")
        input_msg = input("> ")
        first_split = input_msg.split()
        print(proxy.root.exeCommand(input_msg))
        
        if first_split[0] == "quit":
            proxy.root.exeCommand(input_msg)
            sys.exit(0)

if __name__ == '__main__':
    main()