import os
i=0
while True:
	i+=1
	os.system("./gen;./bf;./std")
	if open('stairs.out','r').read()!=open('bf.out','r').read():
		print('WA',i)
		break
	print('AC',i)