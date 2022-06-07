#!/usr/bin/env python3
# Foundations of Python Network Programming, Third Edition
# https://github.com/brandon-rhodes/fopnp/blob/m/py3/chapter03/tcp_sixteen.py
# Simple TCP client and server that send and receive 16 octets

import argparse, socket
import sys
import glob
import time
import os

def recvall(sock, length):
    data = b''
    while len(data) < length:
        more = sock.recv(length - len(data))
        if not more:
            raise EOFError('was expecting %d bytes but only received'
                           ' %d bytes before the socket closed'
                           % (length, len(data)))
        data += more
    return data

def server(interface, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((interface, port))
    sock.listen(1)
    print('Listening at', sock.getsockname())

    while True:
        print('Waiting to accept a new connection')
        sc, sockname = sock.accept()
        print('We have accepted a connection from', sockname)
        print('  Socket name:', sc.getsockname())
        print('  Socket peer:', sc.getpeername())
        #message = recvall(sc, 16)
        
        while True:
            len_msg = recvall(sc, 3)
            message = recvall(sc, int(len_msg))
            print('  Message len:', repr(len_msg))
            print('  Incoming message:', repr(message))

            commands = (message.decode('utf-8')).split()

            if commands[0] == 'ping':
                msg = bytes(" ".join(commands[1:]), 'utf-8')
                len_msg = b'%03d' % (len(msg))
                msg = len_msg + msg
                sc.sendall(msg)

            elif commands[0] == 'ls':
                if len(commands) == 1:
                    directory = glob.glob('*')

                else:
                    directory = glob.glob(commands[1])

                reply = ''

                for i in directory:
                    if i == directory[-1]:
                        reply += i

                    else:
                        reply += i + '\n'

                msg = bytes(reply, 'utf-8')
                len_msg = b'%03d' % (len(msg))
                msg = len_msg + msg

                sc.sendall(msg)

            elif commands[0] == 'get':
                path_file = commands[1]
                path = commands[1]
                name_file = commands[2]
                helper = "/"
                space = " "
                path_file=path_file+helper+name_file

                f=open(path_file,"rb")
                b=f.read()
                length = len(b)

                new_length = b"%03d" % (len(b),) 

                output = path.encode() + space.encode() + new_length + space.encode() + name_file.encode() 
                len_output = b"%03d" % (len(output.decode()),) 
                sc.sendall(len_output)
                sc.sendall(output) 

            elif commands[0] == 'quit':
                sc.sendall(b'Farewell, client')
                sc.close()
                print('  Reply sent, socket closed')
                break

        break

def client(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    print('Client has been assigned socket name', sock.getsockname())
    #sock.sendall(b'Hi there, server')
    #msg = b'Hi there, server'

    while True:
        command = input("> ")
        commands = command.split()

        msg = bytes(command, 'utf-8')
        len_msg = b'%03d' % (len(msg))
        msg = len_msg + msg

        if commands[0] == 'ping':
            if len(commands) == 1:
                print('Missing args for command ping.')
            
            else:
                sock.sendall(msg)
                len_msg = recvall(sock, 3)
                message = recvall(sock, int(len_msg))
                
                print('terima: ' + message.decode('utf-8'))

        elif commands[0] == 'ls':
            sock.sendall(msg)

            len_msg = recvall(sock, 3)
            message = recvall(sock, int(len_msg))

            print(message.decode('utf-8'))

        elif commands[0] == 'get':
            if len(commands) != 3:
                print('Missing args for command get.')
                continue

            sock.sendall(msg)

            len_msg = recvall(sock, 3)
            message = recvall(sock, int(len_msg))

            replies = message.decode()

            replay=replies.split()
            print('Output pada Server:')
            print('Fetch:',replay[0]) 
            print('size :',replay[1])
            print('lokal :',replay[2])

        elif commands[0] == 'quit':
            print('Server shutdown...')
            print('Client shutdown...')
            sock.sendall(msg)
            recvall(sock, 16)
            time.sleep(3)
            sock.close()
            break

        else:
            print('Unknown command. Try again.')

if __name__ == '__main__':
    choices = {'client': client, 'server': server}
    parser = argparse.ArgumentParser(description='Send and receive over TCP')
    parser.add_argument('role', choices=choices, help='which role to play')
    parser.add_argument('host', help='interface the server listens at;'
                        ' host the client sends to')
    parser.add_argument('-p', metavar='PORT', type=int, default=1060,
                        help='TCP port (default 1060)')
    args = parser.parse_args()
    function = choices[args.role]
    function(args.host, args.p)