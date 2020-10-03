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
def getrep(s,d):
	for i in s:
		if i!=' ':
			if i in d:
				d[i]+=1
			else:
				d[i]=1
def readin():
	listf=['010','011','012','101','304','305','306','307','308','309']
	s='';sm=0
	for i in listf:
		fin=open('xin_cmn_200'+i,'rt',encoding='utf-8')
		news,newsm=precut(fin.read())
		s+=news;sm+=newsm
		fin.close()
	return s,sm
def main():
	fout=open('xin.out','wt',encoding='utf-8')
	s,sm=readin()
	d={}
	getrep(s,d)
	print(sm,d,file=fout)
main()