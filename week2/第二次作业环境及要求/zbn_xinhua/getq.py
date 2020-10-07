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
def main():
	fout=open('getq.out','wt',encoding='utf-8')
	s,d,lstr=readin()
	print('train rfc')
	rfc=initrfc(d,lstr);
	print('rfc classify')
	dictq=getq(rfc,d)
	print('output')
	for st,pr in dictq.items():
		print(st,pr,file=fout)
main()
