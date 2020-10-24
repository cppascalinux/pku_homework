import nltk,math,os,pke,string,random
MAXL=5
WORDCOUNT=25
RATE=0.85
THRES=1.35
WORDREP=8
PUNC=set([',','.',':',';','?','(',')','[',']','&','!','*','@','#','$','%','"',"'",'+','-','/','|','<','>','{','}','_','^','`','~'])
tokener=nltk.tokenize.word_tokenize
lemmaer=nltk.stem.WordNetLemmatizer().lemmatize
tager=nltk.pos_tag
def mul(mx,my):
	return [[sum(a*b for a,b in zip(rx,ry)) for ry in zip(*my)] for rx in mx]
def add(mx,my):
	return [[a+b for a,b in zip(rx,ry)] for rx,ry in zip(mx,my)]
def getfiles():
	dir='all_docs_abstacts_refined'
	# print(list(os.walk(dir)))
	return [dir+'/'+x for x in list(os.walk(dir))[0][2] if 'txt' in x]
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
					mat[d[wp[i][0]]][d[wp[j][0]]]+=100/(i-j)**2
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
	words=set(next(zip(*(sorted(list(d.items()),key=lambda x:vec[0][x[1]],reverse=True)[:int(WORDCOUNT)]))))
	nd={}
	print(len(wp))
	for i in range(len(wp)-1):
		wd1,wd2=wp[i][0],wp[i+1][0]
		if wd1 in words and wd2 in words:
			if not wd1 in nd:
				nd[wd1]={}
			if not wd2 in nd[wd1]:
				nd[wd1][wd2]=0
			nd[wd1][wd2]+=1
	for wd1,pd in nd.items():
		for wd2 in pd:
			if pd[wd2]>=WORDREP:
				fout.write(wd1+' '+wd2+'\n')
	# for wd,num in words:
		# f0.037084	fout.write(wd+'\n')
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
def solvetxt(fl):#TextRank
	# fin=open(fl,'rt',encoding='utf8')
	pketxt=pke.unsupervised.TextRank()
	pos={'NOUN','ADJ'}
	pketxt.load_document(input=fl,language='en',normalization=None)
	# pketxt.candidate_selection(pos=pos)
	pketxt.candidate_weighting(pos=pos,top_percent=0.01)
	phrases=pketxt.get_n_best(n=10)
	fout=open(fl[:-4]+'.mykey','wt',encoding='utf8')
	for wd,scr in phrases:
		fout.write(wd+'\n')
def solvesgl(fl):#SingleRank
	pos={'NOUN','PROPN','ADJ'}
	pkesgl=pke.unsupervised.SingleRank()
	pkesgl.load_document(input=fl,language='en',normalization=None)
	pkesgl.candidate_selection(pos=pos)
	pkesgl.candidate_weighting(window=10,pos=pos)
	phrases=pkesgl.get_n_best(n=5)
	fout=open(fl[:-4]+'.mykey','wt',encoding='utf8')
	for wd,scr in phrases:
		fout.write(wd+'\n')
def solvetpc(fl):#TopicRank
	pketpc=pke.unsupervised.TopicRank()
	pketpc.load_document(input=fl)
	pos={'NOUN','PROPN','ADJ'}
	stoplist=list(string.punctuation)
	stoplist+=['-lrb-','-rrb-','-lcb-','-rcb-','-lsb-','-rsb-']
	stoplist+=nltk.corpus.stopwords.words('english')
	pketpc.candidate_selection(pos=pos, stoplist=stoplist)
	pketpc.candidate_weighting(threshold=0.74, method='average')
	phrases=pketpc.get_n_best(n=5)
	fout=open(fl[:-4]+'.mykey','wt',encoding='utf8')
	for wd,scr in phrases:
		fout.write(wd+'\n')
def solvepst(fl):#PositionRank
	pos={'NOUN','PROPN','ADJ'}
	grammar='NP: {<ADJ>*<NOUN|PROPN>+}'
	pkepst=pke.unsupervised.PositionRank()
	pkepst.load_document(input=fl,language='en',normalization=None)
	pkepst.candidate_selection(grammar=grammar,maximum_word_number=3)
	pkepst.candidate_weighting(window=10,pos=pos)
	phrases=pkepst.get_n_best(n=5)
	fout=open(fl[:-4]+'.mykey','wt',encoding='utf8')
	for wd,scr in phrases:
		fout.write(wd+'\n')
def solvemtp(fl):
	pkemtp=pke.unsupervised.MultipartiteRank()
	pkemtp.load_document(input=fl)
	pos={'NOUN','PROPN','ADJ'}
	stoplist=list(string.punctuation)
	stoplist+=['-lrb-','-rrb-','-lcb-','-rcb-','-lsb-','-rsb-']
	stoplist+=nltk.corpus.stopwords.words('english')
	pkemtp.candidate_selection(pos=pos, stoplist=stoplist)
	pkemtp.candidate_weighting(alpha=1.1,threshold=0.74,method='average')
	phrases=pkemtp.get_n_best(n=5)
	fout=open(fl[:-4]+'.mykey','wt',encoding='utf8')
	for wd,scr in phrases:
		fout.write(wd+'\n')
def initdf():
	stoplist=list(string.punctuation)
	pke.compute_document_frequency(input_dir='all_docs_abstacts_refined',output_file='output.tsv.gz',extension='txt',language='en',normalization="stemming",stoplist=stoplist)
def solvetfidf(fl):
	pketf=pke.unsupervised.TfIdf()
	pketf.load_document(input=fl,language='en',normalization=None)
	pketf.candidate_selection(n=3, stoplist=list(string.punctuation))
	df=pke.load_document_frequency_file(input_file='output.tsv.gz')
	pketf.candidate_weighting(df=df)
	phrases=pketf.get_n_best(n=5)
	fout=open(fl[:-4]+'.mykey','wt',encoding='utf8')
	for wd,scr in phrases:
		fout.write(wd+'\n')
def judge(fl):
	key=open(fl[:-4]+'.key','rt',encoding='utf8')
	mykey=open(fl[:-4]+'.mykey','rt',encoding='utf8')
	sk=[x.strip('\n') for x in key.readlines()]
	skm=[x.strip('\n') for x in mykey.readlines()]
	# print(sk,skm)
	stk,stmk=set(),set()
	for wd in sk:
		stk.add(' '.join([lemmaer(x[0],pos=getty(x[1])) for x in tager(tokener(wd.lower()))]))
	for wd in skm:
		stmk.add(' '.join([lemmaer(x[0],pos=getty(x[1])) for x in tager(tokener(wd.lower()))]))
	# print(stk,stmk)
	l1=len(stk)
	l2=len(stmk)
	if l1==0 or l2==0:
		return 0,0,0
	l3=len(stk&stmk)
	# print(l1,l2,l3)
	return l3/l2,l3/l1,2*l3/(l1+l2)
def main():
	initdf()
	ls=getfiles()[:100]
	# ls=['all_docs_abstacts_refined/1040296.txt']
	res=open('result.txt','wt',encoding='utf8')
	ta,tb,tc=0,0,0
	for fl in ls:
		print(fl)
		# solve(fl)
		# solvetxt(fl)
		# solvetpc(fl)
		# solvesgl(fl)
		# solvepst(fl)
		# solvemtp(fl)
		solvetfidf(fl)
		a,b,c=judge(fl)
		ta+=a/len(ls)
		tb+=b/len(ls)
		tc+=c/len(ls)
		res.write(fl[26:]+' P:%.6f R:%.6f F:%.6f\n'%(a,b,c))
		print(fl[26:]+' P:%.6f R:%.6f F:%.6f'%(a,b,c))
	res.write('Average: P:%.6f R:%.6f F:%.6f\n'%(ta,tb,tc))
	print('Average: P:%.6f R:%.6f F:%.6f'%(ta,tb,tc))
main()