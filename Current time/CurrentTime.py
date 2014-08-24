__author__ = 'ipetrash'

import datetime as dt
import time

# https://docs.python.org/3.4/library/datetime.html
# https://docs.python.org/3.4/library/time.html

if __name__ == '__main__':
    while True:
        cur_time = dt.datetime.now().time()
        print("Current time is: %s" % cur_time.strftime("%H:%M:%S"), end='\r')
        time.sleep(0.5)  # every 0.5 second (500 millisecond)