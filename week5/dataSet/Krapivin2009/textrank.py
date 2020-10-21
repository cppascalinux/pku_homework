import nltk,math,os
MAXL=5
WORDCOUNT=10
RATE=0.85
THRES=1.35
PUNC=set([',','.',':',';','?','(',')','[',']','&','!','*','@','#','$','%','"',"'",'+','-','/','|','<','>','{','}','_','^','`','~'])
tokener=nltk.tokenize.word_tokenize
lemmaer=nltk.stem.WordNetLemmatizer().lemmatize
tager=nltk.pos_tag
def mul(mx,my):
	return [[sum(a*b for a,b in zip(rx,ry)) for ry in zip(*my)] for rx in mx]
def add(mx,my):
	return [[a+b for a,b in zip(rx,ry)] for rx,ry in zip(mx,my)]
def getfiles():
	dir='.\\all_docs_abstacts_refined'
	return [dir+'\\'+x for x in list(os.walk(dir))[0][2] if 'txt' in x]
def islegal(s):
	return s[0]=='N' or s[0]=='J'
def getty(s):
	if s[0]=='N':
		return 'n'
	if s[0]=='J':
		return 'a'
	if s[0]=='V':
		return 'v'
	return 'r'
def solve(fl):
	fin=open(fl,'rt',encoding='utf8')
	fout=open(fl[:-4]+'.mykey','wt',encoding='utf8')
	s=fin.read()
	abt=[(lemmaer(x[0],getty(x[1])),x[1]) for x in tager(tokener(s[s.index('--A')+3:s.index('--B')].lower())) if not (x[0] in PUNC or len(x[0])==1)]
	# if len(abt)<=1:
	# 	return
	wp=[(lemmaer(x[0],getty(x[1])),x[1]) for x in tager(tokener(s.lower()))]
	d,tp={},0
	for wd,ty in abt:
		if islegal(ty):
			if not wd in d:
				d[wd]=tp
				tp+=1
	# print('tp:%d'%tp)
	if tp==0:
		return
	mat=[[0]*tp for i in range(tp)]
	# print(mat)
	for i in range(len(wp)):
		if wp[i][0] in d:
			for j in range(i+1,min(i+MAXL+1,len(wp))):
				if wp[j][0] in d:
					mat[d[wp[i][0]]][d[wp[j][0]]]+=100/(i-j)/(i-j)
				elif wp[j][0] in PUNC:
					break
	for i in range(tp):
		sm=sum(mat[i])
		if sm>0:
			for j in range(tp):
				mat[i][j]*=RATE/sm
	# print(mat)
	vec=[[1]*tp]
	ad=[[1-RATE]*tp]
	for i in range(100):
		vec=add(mul(vec,mat),ad)
	words=sorted(list(d.items()),key=lambda x:vec[0][x[1]],reverse=True)
	for wd,num in words:
		fout.write(wd+' '+str(vec[0][num])+'\n')
		# if vec[0][num]>=THRES:
		# 	fout.write(wd+'\n')
	# st=set(list(zip(*words[:15]))[0])
	# vis=set()
	# phrases=[]
	# wp=list(zip(*wp))[0]
	# for i in range(MAXPHRASE,1,-1):
	# 	lst=-1
	# 	for j in range(len(wp)):
	# 		if wp[j] in st and not wp[j] in vis:
	# 			# print('qwq')
	# 			if j-lst==i:
	# 				s=' '.join(wp[lst+1:j+1])
	# 				phrases+=[s]
	# 				for x in wp[lst+1:j+1]:
	# 					vis.add(x)
	# 		else:
	# 			lst=j
	# for pr in phrases:
	# 	fout.write(pr+'\n')
def judge(fl):
	key=open(fl[:-4]+'.key','rt',encoding='utf8')
	mykey=open(fl[:-4]+'.mykey','rt',encoding='utf8')
	sk=[x.strip('\n') for x in key.readlines()]
	skm=[x.strip('\n') for x in mykey.readlines()]
	# print(sk,skm)
	stk,stmk=set(),set()
	for wd in sk:
		list(stk.add(lemmaer(x[0],pos=getty(x[1]))) for x in tager(tokener(wd.lower())))
	for wd in skm:
		s=wd.split(' ')
		list(stmk.add(x) for x in s)
	l1=len(stk)
	l2=len(stmk)
	if l1==0 or l2==0:
		return 0,0,0
	l3=len(stk&stmk)
	# print(l1,l2,l3)
	return l3/l2,l3/l1,2*l3/(l1+l2)
def main():
	ls=getfiles()
	ls=['.\\all_docs_abstacts_refined\\qwq.txt']
	res=open('result.txt','wt',encoding='utf8')
	ta,tb,tc=0,0,0
	for fl in ls:
		print(fl)
		solve(fl)
		a,b,c=judge(fl)
		ta+=a/len(ls)
		tb+=b/len(ls)
		tc+=c/len(ls)
		res.write(fl[28:]+' P:%.6f R:%.6f F:%.6f\n'%(a,b,c))
		print(fl[28:]+' P:%.6f R:%.6f F:%.6f'%(a,b,c))
	res.write('Average: P:%.6f R:%.6f F:%.6f\n'%(ta,tb,tc))
	print('Average: P:%.6f R:%.6f F:%.6f'%(ta,tb,tc))
main()