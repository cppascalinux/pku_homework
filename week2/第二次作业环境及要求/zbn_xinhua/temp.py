import random
fin=open('train.out','rt',encoding='utf-8')
s=fin.readlines()
fin.close()
random.shuffle(s)
fout=open('train.out','wt',encoding='utf-8')
for i in s:
	fout.write(i)