# -*- coding:utf-8 -*-
#defaultdict小测试
import collections
def default_factory():
	return 'default value'
d=collections.defaultdict(default_factory,foo='bar')
print(d)
print("\n")
print(d['foo'])
print(d['bar'])
