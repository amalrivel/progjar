#!/usr/bin/env python3
# Foundations of Python Network Programming, Third Edition
# https://github.com/brandon-rhodes/fopnp/blob/m/py3/chapter07/srv_threaded.py
# Using multiple threads to serve several clients in parallel.

import zen_utils
from threading import Thread

value = 0

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

def start_threads(listener, workers=4):
    t = (listener,)
    for i in range(workers):
        Thread(target=threads, args=t).start()

def handle_request(sock):
    """Receive a single client request on `sock` and send the answer."""
    global value
    len_msg = recvall(sock, 3)
    message = recvall(sock, int(len_msg))
    message = str(message, encoding="ascii")
    arr = message.split()
    if arr[0] == "ADD":
        value += int(arr[1])
    elif arr[0] == "DEC":
        value -= int(arr[1])
    send_message = "Total = : " + str(value)
    len_send_message = b"%03d" % (len(send_message),)
    send_message = len_send_message + bytes(send_message, encoding="ascii")
    sock.sendall(send_message)

def threads(listener):
    """Converse with a client over `sock` until they are done talking."""
    while True:
        sock, address = listener.accept()
        print('Accepted connection from {}'.format(address))
        try:
            while True:
                handle_request(sock)
        except EOFError:
            print('Client socket to {} has closed'.format(address))
        except Exception as e:
            print('Client {} error: {}'.format(address, e))
        finally:
            sock.close()

if __name__ == '__main__':
    address = zen_utils.parse_command_line('multi-threaded server')
    listener = zen_utils.create_srv_socket(address)
    start_threads(listener)