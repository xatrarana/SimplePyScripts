#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# pip install simpleeval
from simpleeval import simple_eval


print(simple_eval("21 + 21"))  # 42
print(simple_eval("2 + 2 * 2"))  # 6
print(simple_eval('10 ** 123'))  # 1000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
print(simple_eval("21 + 19 / 7 + (8 % 3) ** 9"))  # 535.7142857142857

# User functions
print(simple_eval("square(11)", functions={"square": lambda x: x * x}))  # 121

import math
print(simple_eval("abs(sin(3) * cos(3))", functions={'sin': math.sin, 'cos': math.cos, 'abs': abs}))  # 0.13970774909946293


def my_md5(value):
    import hashlib
    return hashlib.md5(bytes(value, 'utf-8')).hexdigest()


print(simple_eval("md5('Hello World!')", functions={'md5': my_md5}))  # ed076287532e86365e841e92bfc50d8c

print(simple_eval("list('1234')", functions={'list': list}))  # ['1', '2', '3', '4']
print(simple_eval("'1,2,3,4'.split(',')"))  # ['1', '2', '3', '4']
