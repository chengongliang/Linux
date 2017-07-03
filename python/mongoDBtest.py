#!/usr/bin/python
# _*_ coding:utf8 _*_
import time
from pymongo import MongoClient
import threading

time1 = time.time()
ip = "127.0.0.1"
port = 28017
conn = MongoClient(ip, port, maxPoolSize=1000)
db = conn.monitor
db.authenticate("monitor", "123qweasd")


def run(num):
    print num
    data = db.monitor.find({'_id': num})
    for i in data:
        print i
    time.sleep(3)


if __name__ == "__main__":
    threads = []
    for num in range(100):
        # print num
        t1 = threading.Thread(target=run, args=(num,))
        t1.start()
        threads.append(t1)

    for t in threads:
        t.join()
    conn.close()
    time2 = time.time()
    print time2 - time1
