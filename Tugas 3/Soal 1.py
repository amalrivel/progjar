#!/usr/bin/env python3
# Foundations of Python Network Programming, Third Edition
# https://github.com/brandon-rhodes/fopnp/blob/m/py3/chapter08/queuepi.py
# Small application that uses several different message queues

import random, threading, time, zmq, sqlite3

def randomizer():
    return str(random.randint(0, 2))

def query(num):
    db = sqlite3.connect("data.db")
    cur = db.cursor()

    total = 0
    value = 0
    n1 = random.randint(1, 99000)
    n2 = random.randint(1, 1000)
    mod = "length(FirstNameLastName)"
    sql = "select count(*) from MOCKDATA where (ID>={} AND ID<={})   = {};".format(n1, n1+n2, mod, num)
    cur.execute(sql)
    value = int(cur.fetchone()[0])
    
    total += value
    hasil = "n1 = {}, n2 = {}, num = {}, hasil = {}".format(n1, n2, num, total)
    db.close()
    return hasil

def generator(zcontext, url):
    """Produce random points in the unit square."""
    zsock = zcontext.socket(zmq.PUB)
    zsock.bind(url)
    while True:
        zsock.send_string(randomizer())

def executor_0(zcontext, in_url, out_url):
    """Coordinates in the lower-left quadrant are inside the unit circle."""
    isock = zcontext.socket(zmq.SUB)
    isock.connect(in_url)
    isock.setsockopt(zmq.SUBSCRIBE, b'0')
    osock = zcontext.socket(zmq.PUSH)
    osock.connect(out_url)
    while True:
        hasil_generator=isock.recv_string()
        hasil = query(hasil_generator)
        osock.send_string(hasil)

def executor_1(zcontext, in_url, out_url):
    """Coordinates in the lower-left quadrant are inside the unit circle."""
    isock = zcontext.socket(zmq.SUB)
    isock.connect(in_url)
    isock.setsockopt(zmq.SUBSCRIBE, b'1')
    osock = zcontext.socket(zmq.PUSH)
    osock.connect(out_url)
    while True:
        hasil_generator=isock.recv_string()
        hasil = query(hasil_generator)
        osock.send_string(hasil)

def executor_2(zcontext, in_url, out_url):
    """Coordinates in the lower-left quadrant are inside the unit circle."""
    isock = zcontext.socket(zmq.SUB)
    isock.connect(in_url)
    isock.setsockopt(zmq.SUBSCRIBE, b'2')
    osock = zcontext.socket(zmq.PUSH)
    osock.connect(out_url)
    while True:
        hasil_generator=isock.recv_string()
        hasil = query(hasil_generator)
        osock.send_string(hasil)

def tally(zcontext, url):
    """Tally how many points fall within the unit circle, and print pi."""
    zsock = zcontext.socket(zmq.PULL)
    zsock.bind(url)
    hasil = zsock.recv_string()
    print(hasil)

def start_thread(function, *args):
    thread = threading.Thread(target=function, args=args)
    thread.daemon = True  # so you can easily Ctrl-C the whole program
    thread.start()

def main(zcontext):
    pubsub = 'tcp://127.0.0.1:6700'
    pushpull = 'tcp://127.0.0.1:6702'
    start_thread(generator, zcontext, pubsub)
    start_thread(executor_0, zcontext, pubsub, pushpull)
    start_thread(executor_1, zcontext, pubsub, pushpull)
    start_thread(executor_2, zcontext, pubsub, pushpull)
    start_thread(tally, zcontext, pushpull)
    time.sleep(5)

if __name__ == '__main__':
    main(zmq.Context())