# -*- coding:utf-8 -*-
#defaultdict小测试
import collections
from random import randrange, choice
def default_factory():
	return 'default value'
d=collections.defaultdict(default_factory,foo='bar')
print(d)
print("\n")
print(d['foo'])
print(d['bar'])

print ([(i,j) for i in range(10) for j in range(8)])