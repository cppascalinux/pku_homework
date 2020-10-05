import math
# from sklearn.ensemble import RandomForestClassifier
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
	lists=[]
	for i in flist:
		fout=open(name+'_cmn_200'+i,'rt',encoding='utf-8')
		s=fout.read().replace('\n','')
		lists+=precut(s)
	return lists
def getfreq(s):
	B=30
	ansd,dw={},{}
	for i in range(len(s)):
		if s[i] in dw:
			dw[s[i]].append(i)
		else:
			dw[s[i]]=[i]
	while len(dw):
		ndw={}
		for i in list(dw.items()):
			if len(i[1])>=B:
				ansd[i[0]]=i[1]
				for j in i[1]:
					if j<len(s)-1:
						nw=i[0]+s[j+1]
						if nw in ndw:
							ndw[nw].append(j+1)
						else:
							ndw[nw]=[j+1]
		dw=ndw
	return ansd
def main():
	fout=open("b.out",'wt',encoding='utf-8')
	lists=readin('xin')
	alls=''.join(lists)
	freqd=getfreq(alls)
	print(len(freqd))
main()