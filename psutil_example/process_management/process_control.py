#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


def func():
    import time
    i = 1

    import threading

    while True:
        print(threading.current_thread(), i)
        i += 1

        time.sleep(1)


if __name__ == '__main__':
    from multiprocessing import Process
    p = Process(target=func)
    p.start()
    print(p.pid)

    import psutil
    process = psutil.Process(p.pid)
    print('is_running:', process.is_running())

    # from process_detail_info import print_info
    # print_info(p.pid)

    import time
    time.sleep(4)

    print('suspend on 3 seconds')
    process.suspend()
    time.sleep(3)

    print('resume')
    process.resume()

    print('terminate after 5 seconds')
    time.sleep(5)

    process.terminate()
    print('terminate')

    result_code = process.wait(timeout=3)
    print('result_code:', result_code)
