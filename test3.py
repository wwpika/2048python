#-*- coding:utf-8 -*-
#zip函数用法示例，合并列表,返回值是个列表list
x=[0,0,0,2]
y=[0,0,4,0]
z=[0,8,0,0]
j=[16,0,0,0]
re=zip(x,y,z,j)
print(list(re)) #[(1, 4, 7), (2, 5, 8), (3, 6, 9)]

'''
#list循环示例
li=[1,9,8,4]
print([elem*2 for elem in li])#[2, 18, 16, 8]

#[::-1]示范
s='hello world\n'
print(s[::-1])


print([[0 for i in range(10)] for j in range(6)])
'''