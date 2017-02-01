#-*- coding:utf-8 -*-
#*，所有多余的参数作为一个元祖存储在args中
#pow(x,y)，返回x的y次方
def powersum(power,*args):
	total=0
	for i in args:
		total+=pow(i,power)
	return total
print ('powersum(2,3,4)==',powersum(2,3,4))
print ('powersum(2,10)==',powersum(2,10))
