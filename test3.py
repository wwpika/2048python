#-*- coding:utf-8 -*-
#zip函数用法示例，合并列表,返回值是个列表list
x=[1,2,3]
y=[4,5,6]
z=[7,8,9]
re=zip(x,y,z)
print(re) #[(1, 4, 7), (2, 5, 8), (3, 6, 9)]

#list循环示例
li=[1,9,8,4]
print([elem*2 for elem in li])#[2, 18, 16, 8]

#[::-1]示范
s='hello world\n'
print(s[::-1])


print([0 for i in range(10)])