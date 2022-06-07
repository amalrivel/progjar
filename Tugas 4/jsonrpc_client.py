# Foundations of Python Network Programming, Third Edition
# https://github.com/brandon-rhodes/fopnp/blob/m/py3/chapter18/jsonrpc_client.py
# JSON-RPC client needing "pip install jsonrpclib-pelix"

from fileinput import close
from jsonrpclib import Server
import time

def main():
    proxy = Server('http://localhost:7002')
    masukan = ""
    while (masukan != "quit"):
        print('Input Client :')
        masukan = input("> ")
        first_split = masukan.split()
        # print(proxy.lengths(masukan))

        if first_split[0] == "get":
            # print(proxy.lengths(masukan))
            replay = proxy.lengths(masukan)
            replay_1=replay.split()
            print('Output pada Server:')
            print('Fetch:',replay_1[0]) 
            print('size :',replay_1[1])
            print('lokal :',replay_1[2])

        elif first_split[0] == "ls":
            if len(first_split) == 1:
                print(proxy.lengths(masukan))

            elif len(first_split) == 2:
                print(proxy.lengths(masukan))

        elif first_split[0] == "ping":
            print(proxy.lengths(masukan))

        elif first_split[0] == "count":
            print('Banyaknya File :', proxy.lengths(masukan))

        elif first_split[0] == "quit":
            print("Bye bye")
            proxy.tutup()
            proxy.close()
            time.sleep(2)

        else:
            print("No Command, please retry\n==========================\n")

if __name__ == '__main__':
    main()
