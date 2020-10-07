def main():
	din=open('dict.out','rt',encoding='utf-8')
	sin=open('copora.out','rt',encoding='utf-8')
	qin=open('getq.out','rt',encoding='utf-8')
	lout=open('label.out','wt',encoding='utf-8')
	sout=open('copora_cpp.out','wt',encoding='utf-8')
	listd=din.readlines()
	num,nwd={},[]
	rep,req={},{}
	num[' ']=0
	nwd+=[' ']
	sm=0
	for ln in listd:
		listw=ln.split(' ')
		rep[listw[0]]=listw[1]
		if len(listw[0])==1:
			sm+=1
			ts=listw[0]
			num[ts]=sm
			nwd+=[ts]
	for i in range(len(nwd)):
		lout.write(str(i)+' '+nwd[i]+'\n')
	s=sin.read()
	sout.write(str(len(s))+'\n')
	for wd in s:
		sout.write(str(num[wd])+' ')
	sout.write('\n')
	listq=qin.readlines()
	for ln in listq:
		listw=ln.split(' ')
		req[listw[0]]=listw[1][:-1]
	sout.write(str(len(rep))+'\n')
	for wd in rep:
		sq='1' if len(wd)==1 else req[wd]
		sout.write(str(len(wd))+' ')
		for ch in wd:
			sout.write(str(num[ch])+' ')
		sout.write(rep[wd]+' '+sq+'\n')
main()