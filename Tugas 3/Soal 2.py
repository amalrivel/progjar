#!/usr/bin/env python3
# Foundations of Python Network Programming, Third Edition
# https://github.com/brandon-rhodes/fopnp/blob/m/py3/chapter08/queuepi.py
# Small application that uses several different message queues

import random, threading, time, zmq, sqlite3

def randomizer():
    return str(random.randint(0, 1))

def query(num):
    db = sqlite3.connect("data.db")
    cur = db.cursor()

    total = 0
    value = 0
    n1 = random.randint(1, 99000)
    n2 = random.randint(1, 1000)
    mod = "length(FirstNameLastName)"
    sql = "select count(*) from MOCKDATA where (ID>={} AND ID<={}) AND {} % 3 = {};".format(n1, n1+n2, mod, num)
    h = hash(sql)
    if h % 2 == 0:
        hasil = "n1 = {}, n2 = {}, num = {}, hasil = nol".format(n1, n2, num)
    else:
        cur.execute(sql)
        value = int(cur.fetchone()[0])
    
    total += value
    hasil = "n1 = {}, n2 = {}, num = {}, hasil = {}".format(n1, n2, num, total)
    db.close()
    return hasil

def generator(zcontext, url, log_url):
    """Produce random points in the unit square."""
    zsock = zcontext.socket(zmq.REQ)
    zsock.bind(url)
    osock = zcontext.socket(zmq.PUSH)
    osock.connect(log_url)
    while True:
        zsock.send_string(randomizer())
        hasil = zsock.recv_string()
        osock.send_string(hasil)

def executor(zcontext, url):
    """Return the sum-of-squares of number sequences."""
    zsock = zcontext.socket(zmq.REP)
    for prefix in b'0', b'1':
        zsock.setsockopt(zmq.IDENTITY, prefix)
    zsock.connect(url)
    while True:
        hasil_generator = zsock.recv_string()
        hasil = query(hasil_generator)
        zsock.send_string(hasil)

def executor_1(zcontext, url):
    """Return the sum-of-squares of number sequences."""
    zsock = zcontext.socket(zmq.REP)
    zsock.setsockopt(zmq.HWM , b'1')
    zsock.connect(url)
    while True:
        hasil_generator = zsock.recv_string()
        hasil = query(hasil_generator)
        zsock.send_string(hasil)
        print("executor_1 berjalan")

def tally(zcontext, url):
    """Tally how many points fall within the unit circle, and print pi."""
    zsock = zcontext.socket(zmq.PULL)
    zsock.bind(url)
    hasil = zsock.recv_string()
    print(hasil)

def start_thread(function, *args):
    thread = threading.Thread(target=function, args=args)
    thread.daemon = True
    thread.start()

def main(zcontext):
    reqrep = 'tcp://127.0.0.1:6701'
    pushpull = 'tcp://127.0.0.1:6702'
    start_thread(generator, zcontext, reqrep, pushpull)
    start_thread(executor, zcontext, reqrep)
    start_thread(tally, zcontext, pushpull)
    time.sleep(5)

if __name__ == '__main__':
    main(zmq.Context())