import os
n,m,h=200000,200000,1000000000
ls=[0,(10,10,h),(n,m,2),(n,m,3),(2000,2000,h),(n,m,h)]
for i in range(1,6):
	os.system(f'mkdir data/subtask{i}')
	for j in range(10):
		# os.system(f'./gen {ls[i][0]} {ls[i][1]} {ls[i][2]}')
		# os.system('./std')
		# os.system(f'cp stairs.in data/subtask{i}/{j}.in')
		# os.system(f'cp stairs.out data/subtask{i}/{j}.out')
		with open(f'data/subtask{i}/{j}.in','r') as fp:
			s='\n'.join([x.strip(' \n') for x in fp.readlines()])+'\n'
		with open(f'data/subtask{i}/{j}.in','w') as fp:
			fp.write(s)
		# os.system(f'./val < data/subtask{i}/{j}.in')