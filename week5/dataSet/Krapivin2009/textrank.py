import nltk,math,os,pke,string,random
MAXL=5#窗口长度
WORDCOUNT=25#用排名前25的单词去构建词组
RATE=0.85#平滑因子
WORDREP=8#输出出现次数>=8的词组
PUNC=set([',','.',':',';','?','(',')','[',']','&','!','*','@','#','$','%','"',"'",'+','-','/','|','<','>','{','}','_','^','`','~'])#英文标点符号
tokener=nltk.tokenize.word_tokenize
lemmaer=nltk.stem.WordNetLemmatizer().lemmatize
tager=nltk.pos_tag
def mul(mx,my):#矩阵乘
	return [[sum(a*b for a,b in zip(rx,ry)) for ry in zip(*my)] for rx in mx]
def add(mx,my):#矩阵加
	return [[a+b for a,b in zip(rx,ry)] for rx,ry in zip(mx,my)]
def getfiles():#得到所有文件名
	dir='all_docs_abstacts_refined'
	return [dir+'/'+x for x in list(os.walk(dir))[0][2] if 'txt' in x]
def islegal(s):#判断是否为名词/形容词
	return s[0]=='N' or s[0]=='J'
def getty(s):#同种词性,转化为不同表示
	if s[0]=='N':
		return 'n'
	if s[0]=='J':
		return 'a'
	if s[0]=='V':
		return 'v'
	return 'r'
def solve(fl):#自己实现的TextRank
	fin=open(fl,'rt',encoding='utf8')
	fout=open(fl[:-4]+'.mykey','wt',encoding='utf8')
	s=fin.read()
	abt=[(lemmaer(x[0],getty(x[1])),x[1]) for x in tager(tokener(s[s.index('--A')+3:s.index('--B')].lower())) if not (x[0] in PUNC or len(x[0])==1)]#摘要部分,从这里提取可能的关键词
	wp=[(lemmaer(x[0],getty(x[1])),x[1]) for x in tager(tokener(s.lower()))]#整篇文章,利用这个建图
	d,tp={},0
	for wd,ty in abt:#统计所有可能关键词,并标号
		if islegal(ty):
			if not wd in d:
				d[wd]=tp
				tp+=1
	if tp==0:
		return
	mat=[[0]*tp for i in range(tp)]
	for i in range(len(wp)):#为每个点连边
		if wp[i][0] in d:
			for j in range(max(0,i-MAXL),min(i+MAXL+1,len(wp))):
				if i==j:
					continue
				if wp[j][0] in d:
					mat[d[wp[i][0]]][d[wp[j][0]]]+=100/(i-j)**2#平方反比
				elif wp[j][0] in PUNC:
					break
	for i in range(tp):#矩阵的行归一化
		sm=sum(mat[i])
		if sm>0:
			for j in range(tp):
				mat[i][j]*=RATE/sm
	vec=[[1]*tp]
	ad=[[1-RATE]*tp]
	for i in range(100):#矩阵乘法
		vec=add(mul(vec,mat),ad)
	words=set(next(zip(*(sorted(list(d.items()),key=lambda x:vec[0][x[1]],reverse=True)[:int(WORDCOUNT)]))))#取出前25大的词
	nd={}
	print(len(wp))
	for i in range(len(wp)-1):#回到原文中,统计二字短语的出现次数
		wd1,wd2=wp[i][0],wp[i+1][0]
		if wd1 in words and wd2 in words:
			if not wd1 in nd:
				nd[wd1]={}
			if not wd2 in nd[wd1]:
				nd[wd1][wd2]=0
			nd[wd1][wd2]+=1
	for wd1,pd in nd.items():#输出出现次数>=8的短语
		for wd2 in pd:
			if pd[wd2]>=WORDREP:
				fout.write(wd1+' '+wd2+'\n')
def solvetxt(fl):#TextRank
	pketxt=pke.unsupervised.TextRank()
	pos={'NOUN','ADJ'}
	pketxt.load_document(input=fl,language='en',normalization=None)
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
def solvemtp(fl):#MultipartiteRank
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
def initdf():#get df frome files
	stoplist=list(string.punctuation)
	pke.compute_document_frequency(input_dir='all_docs_abstacts_refined',output_file='output.tsv.gz',extension='txt',language='en',normalization="stemming",stoplist=stoplist)
def solvetfidf(fl):#TF-IDF
	pketf=pke.unsupervised.TfIdf()
	pketf.load_document(input=fl,language='en',normalization=None)
	pketf.candidate_selection(n=3, stoplist=list(string.punctuation))
	df=pke.load_document_frequency_file(input_file='output.tsv.gz')
	pketf.candidate_weighting(df=df)
	phrases=pketf.get_n_best(n=5)
	fout=open(fl[:-4]+'.mykey','wt',encoding='utf8')
	for wd,scr in phrases:
		fout.write(wd+'\n')
def judge(fl):#计算Purity,Recall,F-score
	key=open(fl[:-4]+'.key','rt',encoding='utf8')
	mykey=open(fl[:-4]+'.mykey','rt',encoding='utf8')
	sk=[x.strip('\n') for x in key.readlines()]
	skm=[x.strip('\n') for x in mykey.readlines()]
	stk,stmk=set(),set()
	for wd in sk:#对标准答案提取词干
		stk.add(' '.join([lemmaer(x[0],pos=getty(x[1])) for x in tager(tokener(wd.lower()))]))
	for wd in skm:#对我输出的答案提取词干
		stmk.add(' '.join([lemmaer(x[0],pos=getty(x[1])) for x in tager(tokener(wd.lower()))]))
	l1=len(stk)
	l2=len(stmk)
	if l1==0 or l2==0:
		return 0,0,0
	l3=len(stk&stmk)
	return l3/l2,l3/l1,2*l3/(l1+l2)
def main():
	# initdf()
	ls=getfiles()[:100]
	res=open('result.txt','wt',encoding='utf8')
	ta,tb,tc=0,0,0
	for fl in ls:
		print(fl)
		solve(fl)
		# solvetxt(fl)
		# solvetpc(fl)
		# solvesgl(fl)
		# solvepst(fl)
		# solvemtp(fl)
		# solvetfidf(fl)
		a,b,c=judge(fl)
		ta+=a/len(ls)
		tb+=b/len(ls)
		tc+=c/len(ls)
		res.write(fl[26:]+' P:%.6f R:%.6f F:%.6f\n'%(a,b,c))
		print(fl[26:]+' P:%.6f R:%.6f F:%.6f'%(a,b,c))
	res.write('Average: P:%.6f R:%.6f F:%.6f\n'%(ta,tb,tc))
	print('Average: P:%.6f R:%.6f F:%.6f'%(ta,tb,tc))
main()