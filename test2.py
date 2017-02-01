#-*- coding:utf-8 -*-
#**，所有多余的参数被认为是一个字典的键值对
def findad(username,**args):
	print ('hello:',username)
	for name,address in args.items():
		print ('Contact %s at %s ' %(name,address))
findad('wcdj',gerry='gerry@byteofpython.info',wcdj='wcdj@126.com',yj='yj@gmail.com')