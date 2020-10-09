import math,gc
def ishanzi(s):
	return '\u4e00'<=s<='\u9fff'
def precut(s):
	flag,temps,rslist=0,'',[]
	for i in range(len(s)):
		if ishanzi(s[i]):
			temps+=s[i]
			flag=1
		else:
			if flag:
				flag=0
				temps+=' '
			if s[i:i+6]=='</DOC>':
				rslist.append(temps)
				temps=''
	return rslist
def readin(name):
	flist=['010','011','012','101','304','305','306','307','308','309']
	lists=[' ']
	for i in flist:
		fout=open(name+'_cmn_200'+i,'rt',encoding='utf-8')
		s=fout.read().replace('\n','')
		lists+=precut(s)
	return lists
def getfreq(s):
	B=3
	ansd,dw={},{}
	for i in range(len(s)):
		if s[i]!=' ':
			if s[i] in dw:
				dw[s[i]].append(i)
			else:
				dw[s[i]]=[i]
	while len(dw):
		ndw={}
		for st,ls in dw.items():
			if len(ls)>=B:
				ansd[st]=ls
				for i in ls:
					if i<len(s)-1 and s[i+1]!=' ':
						nw=st+s[i+1]
						if nw in ndw:
							ndw[nw].append(i+1)
						else:
							ndw[nw]=[i+1]
			elif len(st)==1:
				ansd[st]=ls
		dw=ndw
	return ansd
def getpmi(freqd,ftrd):
	n=0
	for st,ls in freqd.items():
		n+=len(ls)
	for st,ls in freqd.items():
		ftrd[st]=[len(ls)]
		mnpmi=math.inf
		p=len(ls)/n
		for i in range(len(st)-1):
			lp,rp=len(freqd[st[:i+1]])/n,len(freqd[st[i+1:]])/n
			mnpmi=min(mnpmi,math.log2(p/lp/rp))
		ftrd[st]+=[mnpmi,p*mnpmi]
def getidf(lists,freqd,ftrd):
	qry=[]
	n=len(lists)
	for i in range(n):
		st=lists[i]
		qry+=[i]*len(st)
	for st,ls in freqd.items():
		tempd={}
		for i in ls:
			tempd[qry[i]]=1
		idf=math.log2(n/len(tempd))
		ftrd[st]+=[idf]
def geth(s,freqd,ftrd):
	for st,ls in freqd.items():
		ld,rd={},{}
		sm=len(ls)
		lh,rh=0,0
		for i in ls:
			ts=s[i+1]
			if ts in rd:
				rd[ts]+=1
			else:
				rd[ts]=1
			ts=s[i-len(st)]
			if ts in ld:
				ld[ts]+=1
			else:
				ld[ts]=1
		for rst,num in rd.items():
			p=num/sm
			rh+=p*math.log2(p)
		for lst,num in ld.items():
			p=num/sm
			lh+=p*math.log2(p)
		ftrd[st]+=[min(-lh,-rh)]

def getde(ftrd):
	for st,ls in ftrd.items():
		sm=0
		for wd in st:
			if wd=='的':
				sm+=1
		ftrd[st]+=[sm]
def main():
	fout=open('dict.out','wt',encoding='utf-8')
	sout=open('copora.out','wt',encoding='utf-8')
	print('readin')
	lists=readin('zbn')
	alls=''.join(lists)
	sout.write(alls)
	print('getfreq')
	freqd=getfreq(alls)
	print(len(freqd))
	ftrd={}
	gc.collect();
	print('getpmi')
	getpmi(freqd,ftrd)
	gc.collect();
	print('getidf')
	getidf(lists,freqd,ftrd)
	gc.collect();
	print('geth')
	geth(alls,freqd,ftrd)
	gc.collect();
	print('getde')
	getde(ftrd)
	print('output')
	for st,ls in ftrd.items():
		print(st,end=' ',file=fout)
		for i in ls:
			print(i,end=' ',file=fout)
		print('',file=fout)
main()