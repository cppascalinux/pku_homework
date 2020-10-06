import math,numpy
from sklearn.ensemble import RandomForestClassifier
def readin():
	ftrain=open('train.out','rt',encoding='utf-8')
	fdict=open('dict.out','rt',encoding='utf-8')
	fcop=open('copora.out','rt',encoding='utf-8')
	s=fcop.read()
	d={}
	for ts in fdict.readlines():
		templ=ts.split(' ')
		# print(templ)
		d[templ[0]]=[float(x) for x in templ[1:-1]]
	lstr=[x.split(' ')[0:2] for x in ftrain.readlines()]
	return s,d,lstr
def initrfc(d,lstr):
	lx=[d[x[0]][1:] for x in lstr]
	ly=[x[1] for x in lstr]
	rfc=RandomForestClassifier(n_jobs=-1)
	rfc.fit(lx,ly)
	return rfc
def getq(rfc,d):
	lsd=[x for x in d.items() if len(x[0])>1]
	qrx=[x[1][1:] for x in lsd]
	qry=rfc.predict_proba(qrx);
	dictq={}
	for i in range(len(lsd)):
		dictq[lsd[i][0]]=qry[i][1]
	return dictq
def getfreq(d):
	sm=[0]*100
	freq={}
	for st,ls in d.items():
		sm[len(st)]+=ls[0]
	for st,ls in d.items():
		freq[st]=ls[0]/sm[len(st)]
	return freq
def dp(s,dictq,freq,alpha):
	MAXL=50
	n=len(s)
	f=[1]+[-1]*n
	g=[0]*(n+1)
	for i in range(1,n):
		if i%10000==0:
			print(i)
		if s[i]==' ':
			f[i]=f[i-1]
			g[i]=g[i-1]
			continue;
		for j in range(1,MAXL):
			p,k=0,i-j
			wd=s[k+1:i+1]
			if j==1:
				p=freq[wd] if wd in freq else 2/n
			elif not wd in dictq:
				p=0
				break
			else:
				p=alpha**(1-j)*freq[wd]*dictq[wd]
			if f[i]<f[k]*p:
				f[i],g[i]=f[k]*p,k
			if s[k]==' ':
				break
	ansl=[]
	ptr=n-1
	while ptr>0:
		wd=s[g[ptr]+1:ptr+1]
		if wd!=' ':
			ansl+=[s[g[ptr]+1:ptr+1]]
		ptr=g[ptr]
	ansl.reverse()
	return ansl
def main():
	fout=open('solve.out','wt',encoding='utf-8')
	s,d,lstr=readin()
	print('train rfc')
	rfc=initrfc(d,lstr);
	print('rfc classify')
	dictq=getq(rfc,d)
	print('get theta')
	freq=getfreq(d)
	print('dp')
	ansl=dp(s,dictq,freq,1.5)
	print('output')
	for i in ansl:
		print(i,end=' ',file=fout)
main()
