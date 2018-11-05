import re
import matplotlib.pyplot as plt
import numpy as np
import sys
from subprocess import call



def read_write(xxx,yyy):
	mesh=open('dumpfile.%d.%d.txt'%(xxx,yyy))
	Q_tempo=np.zeros(100)
	N=list()

	for line in mesh:
		line=line.rstrip()
		if re.search('[0-9]+[.][0-9]+ [0-9]+[.][0-9]+ [0-9]+ [0-9]+',line):
			num=line.split()
			N.append(int(num[3]))

	N_timesofvisit=np.asarray(N)
	for i in range(len(N_timesofvisit)):
		for j in range(1,len(Q_tempo)):
			if(N_timesofvisit[i]==j): Q_tempo[j]+=1
	Q_tempo[0]=90000-sum(Q_tempo)

	with open('charge.%d.%d.txt'%(xxx,yyy),'w') as f:
		for i in range(1,len(Q_tempo)):
			print('%d  %d\n'%(i,Q_tempo[i]),file=f)
		print('total number = %f'%sum(Q_tempo), file=f)

	return Q_tempo

def average(i,N_data):
	Q_ave=np.zeros(100)
	Q_tem=np.zeros(100)
	Q_sum=np.zeros(100)

	if(N_data==9):
		for j in range(N_data):
			Q_tem=read_write(i,j+1)
			for k in range(100):
				Q_sum[k]+=Q_tem[k]
		for k in range(100):
			Q_ave[k]=Q_sum[k]/N_data

	else:
		for j in range(N_data):
			Q_tem=read_write(i,j)
			for k in range(100):
				Q_sum[k]+=Q_tem[k]
		for k in range(100):
			Q_ave[k]=Q_sum[k]/N_data

	print(Q[:][1])
	return Q_ave

Q=np.zeros((5,100))

Q[0][:]=average(1,9) ## array
Q[1][:]=average(2,10)
Q[2][:]=average(3,10)
Q[3][:]=average(4,10)
Q[4][:]=average(5,10)

t=np.arange(100)
c=['b--','bs','b^','g--','gs','g^','r--','rs','r^'] ## c is a list

for i in range(5):
	plt.plot(t[1:100],Q[i][1:100],c[i])



plt.xscale('linear')
plt.yscale('log')
plt.legend()
plt.show()
