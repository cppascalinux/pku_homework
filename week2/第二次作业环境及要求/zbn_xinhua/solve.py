import math,gc
def readin():
	sin=open('copora.out','rt',encoding='utf-8')
	din=open('dict.out','rt',encoding='utf-8')
	qin=open('getq.out','rt',encoding='utf-8')
	s=sin.read()
	d={}
	while True:
		temps=din.readline()
		if temps!='':
			templ=temps.split(' ')
			d[templ[0]]=[int(templ[1]),1]
		else:
			break
	while True:
		temps=qin.readline()
		if temps!='':
			templ=temps.split(' ')
			d[templ[0]][1]=max(0.01,float(templ[1]))
		else:
			break
	return s,d;
def getfreq(d):
	sm=[0]*100
	for st,ls in d.items():
		sm[len(st)]+=ls[0]
	for st,ls in d.items():
		d[st]+=[ls[0]/sm[len(st)]]
def dp(s,d,alpha,autorl=True):
	MAXL=50
	n=len(s)
	f=[0]+[-math.inf]*n
	g=[0]*(n+1)
	for i in range(1,n):
		if i%100000==0:
			print(i)
		if s[i]==' ':
			f[i]=f[i-1]
			g[i]=i-1
			continue
		for j in range(1,min(MAXL,i+1)):
			p,k=0,i-j
			wd=s[k+1:i+1]
			if wd in d:
				ls=d[wd]
				p=alpha**(1-j)*ls[1]*ls[2]
				if p<=0:
					continue
				p=math.log2(p)
			else:
				break
			if f[i]<f[k]+p:
				f[i],g[i]=f[k]+p,k
			if s[k]==' ':
				break
	tf=f[n-1]
	del f
	if autorl:
		gc.collect()
	ansl=[]
	ptr=n-1
	while ptr>0:
		wd=s[g[ptr]+1:ptr+1]
		if wd!=' ':
			ansl+=[s[g[ptr]+1:ptr+1]]
		ptr=g[ptr]
	ansl.reverse()
	return ansl,tf
def vt(s,d,alpha):
	for times in range(5):
		print('-------------------------------------------{}------------------------------------------'.format(times))
		sm=[0]*100
		ns=dp(s,d,alpha)[0]
		tempd={}
		for wd in d:
			d[wd][0]=0
		for wd in ns:
			sm[len(wd)]+=1
			if wd in tempd:
				tempd[wd]+=1
			else:
				tempd[wd]=1
		for wd in ns:
			d[wd][2]=tempd[wd]/sm[len(wd)]
		del sm,ns,tempd
		gc.collect()
def getalpha(s,d,rate0):
	ftrain=open('train.out','rt',encoding='utf-8')
	ls=[x.split(' ')[0] for x in ftrain.readlines() if x.split(' ')[1]=='1']
	n=len(ls)
	l,r=0,200
	for times in range(20):
		alpha=(l+r)/2
		rm=int(rate0*n)
		vt(s,d,alpha)
		for wd in ls:
			if len(dp(wd,d,alpha,False)[0])==1:
				rm-=1
		if rm>=0:
			r=alpha
		else:
			l=alpha
	return (l+r)/2
def solve(s,d):
	alpha=3
	sout=open('cuts.out','wt',encoding='utf-8')
	wout=open('words.out','wt',encoding='utf-8')
	fout=open('features.out','wt',encoding='utf-8')
	alpha=getalpha(s,d,0.95)
	# vt(s,d,1)
	ansl=dp(s,d,alpha)[0]
	for wd in ansl:
		sout.write(wd+' ')
	tempd={}
	for wd in ansl:
		if wd in tempd:
			tempd[wd]+=1
		else:
			tempd[wd]=1
	wordls=list(tempd.items())
	cmp=lambda x:x[1]
	wordls.sort(key=cmp,reverse=True)
	for wd,q in wordls:
		if len(wd)>1:
			wout.write(wd+' '+str(q)+'\n')
	for wd,ls in d.items():
		p0=alpha**(1-len(wd))*ls[1]*ls[2]
		p1=2**(dp(wd,d,alpha,False)[1])
		va=math.log2(p0/p1) if p0>0 else -math.nan
		vb=p0*va
		fout.write(wd+' '+str(va)+' '+str(vb)+'\n')
def main():
	print('readin')
	s,d=readin()
	getfreq(d)
	solve(s,d)
main()