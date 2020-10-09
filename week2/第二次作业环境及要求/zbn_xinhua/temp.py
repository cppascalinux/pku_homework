import random
fin=open('words.out','rt',encoding='utf-8')
lst=fin.readlines()
fin.close()
fout=open('words_temp.out','wt',encoding='utf-8')
for s in lst:
	if not '的' in s:
		fout.write(s)