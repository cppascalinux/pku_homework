# import jieba
import math
def ishanzi(s):
	return '\u4e00'<=s<='\u9fff'
def precut(s):
	s=s.replace('\n','')
	sm=0
	newl=[]
	flag=0
	for i in s:
		if ishanzi(i):
			flag=0
			sm+=1
			newl.append(i)
		elif flag==0:
			flag=1
			newl.append(' ')
	return ''.join(newl),sm
def readin():
	listf=['010','011','012','101','304','305','306','307','308','309']
	s='';sm=0
	for i in listf:
		fin=open('xin_cmn_200'+i,'rt',encoding='utf-8')
		news,newsm=precut(fin.read())
		s+=news;sm+=newsm
		fin.close()
	return s,sm
def getrep(s,d):
	for i in s:
		if i!=' ':
			if i in d:
				d[i]+=1
			else:
				d[i]=1
def getrepc(s,d):
	for i in range(len(s)-1):
		if s[i]!=' ' and s[i+1]!=' ':
			nwd=s[i:i+2]
			if nwd in d:
				d[nwd]+=1
			else:
				d[nwd]=1
def t_test(s,pos,d):
	rpl,lwd=(1,0) if pos==0 or s[pos-1]==' ' else (d[s[pos-1]],d[s[pos-1:pos+1]])
	rpr,rwd=(1,0) if pos==len(s)-1 or s[pos+1]==' ' else (d[s[pos]],d[s[pos:pos+2]])
	if s[pos]==0 or lwd==rwd==0:
		return 0
	return (rwd/rpr-lwd/rpl)/(lwd/rpl**2+rwd/rpr**2)**0.5
def t_cut(s,d):
	cutp,cutw=[],[]
	t=len(s)-1
	for i in range(t):
		if i%100000==0:
			print('1:{}'.format(i))
		if s[i]==' ' or s[i+1]==' ':
			cutp.append(i)
		else:
			delta=t_test(s,i,d)-t_test(s,i+1,d)
			if(delta<-5):
				cutp.append(i)
	print('qwqwqwqwqwqwqwqwq')
	cutp.append(len(s)-1)
	ls=0
	for i in cutp:
		ns=s[ls:i+1]
		ls=i+1
		if ns!=' ':
			cutw.append(ns)
	return cutw
def h_pre(s):
	dpre,dnext={},{}
	for i in range(len(s)):
		if s[i]!=' ':
			if not s[i] in dpre:
				dnext[s[i]]=dpre[s[i]]={}
			if s[i-1]!=' ':
				if s[i-1] in dpre[s[i]]:
					dpre[s[i]][s[i-1]]+=1
				else:
					dpre[s[i]][s[i-1]]=1
			if s[i+1]!=' ':
				if s[i+1] in dnext[s[i]]:
					dnext[s[i]][s[i+1]]+=1
				else:
					dnext[s[i]][s[i+1]]=1
	hpre,hnext={},{}
	for i in list(dpre.items()):
		ns=i[0]
		# print(ns)
		sm,smh=0,0.01
		for j in list(i[1].values()):
			sm+=j
		for j in list(i[1].values()):
			smh+=j/sm*math.log2(sm/j)
		hpre[ns]=smh
	for i in list(dnext.items()):
		ns=i[0]
		# print(ns)
		sm,smh=0,0.01
		for j in list(i[1].values()):
			sm+=j
		for j in list(i[1].values()):
			smh+=j/sm*math.log2(sm/j)
		hnext[ns]=smh
	return hpre,hnext
def h_test(s,pos,d,hpre,hnext):
	if s[pos]==' ':
		return 0
	vp=0 if pos==0 or s[pos-1]==' ' else d[s[pos-1:pos+1]]/d[s[pos]]/hpre[s[pos]]
	vn=0 if pos==len(s)-1 or s[pos+1]==' ' else d[s[pos:pos+2]]/d[s[pos]]/hnext[s[pos]]
	return (vn-vp)*1000;
def h_cut(s,d,hpre,hnext):
	cutp,cutw=[],[]
	t=len(s)-1
	for i in range(t):
		if i%100000==0:
			print('1:{}'.format(i))
		if s[i]==' ' or s[i+1]==' ':
			cutp.append(i)
		else:
			delta=h_test(s,i,d,hpre,hnext)-h_test(s,i+1,d,hpre,hnext)
			if(delta<0):
				cutp.append(i)
	print('qwqwqwqwqwqwqwqwq')
	cutp.append(len(s)-1)
	ls=0
	for i in cutp:
		ns=s[ls:i+1]
		ls=i+1
		if ns!=' ':
			cutw.append(ns)
	return cutw
def jb_cut(s):
	cl=jieba.lcut(s)
	nl=[]
	for i in cl:
		if i!=' ':
			nl.append(i)
	return nl
def output(ls,fl):
	print(len(ls),file=fl)
	for i in range(10000):
		if ls[i]!=' ':
			print(ls[i],end=' ',file=fl)
def main():
	fout=open('xin.out','wt',encoding='utf-8')
	# jbout=open('jieba.out','wt',encoding='utf-8')
	# hjqout=open('hjq.out','wt',encoding='utf-8')
	s,sm=readin()
	# print(s,file=fout)
	d={}
	getrep(s,d)
	getrepc(s,d)
	fw=t_cut(s,d)
	output(fw,fout)
	# hpre,hnext=h_pre(s);
	# hcw=h_cut(s,d,hpre,hnext)
	# output(hcw,hjqout)
	# for i in range(10000):
	# 	print(s[i-2:i+3],h_test(s,i,d,hpre,hnext),file=fout)
	# jbw=jb_cut(s)
	# output(jbw,jbout)
	# print(jbw[0:10000],file=jbout)
	# for i in range(1,1000):
	# 	if s[i]!=' ':
	# 		print(s[i-2:i+3],t_test(s,i,d),file=fout)
	# print(t_test(s,3,d),file=fout)
	# print(sm,d,file=fout)
main()