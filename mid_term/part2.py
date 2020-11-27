import jieba,os,re
def remove_punc(s):#去除标点符号
	t=''
	punc='~`!@#$%^&*()_-+={|[]\\:";<>?,./\'}，）（！：“”；‘’'
	for i in s:
		if not i in punc:
			t+=i
	return t
def is_hanzi(s):#判断一个字符是否为汉字
	return '\u4e00'<=s<='\u9fff'
def is_eng(s):#判断一个字符是否为英文
	return 'a'<=s<='z' or 'A'<=s<='Z'
def main1(list_pair):#根据分词结果构造中英文平行语料
	en_txt=open('english','w',encoding='utf8')#输出的英文语料
	zh_txt=open('chinese','w',encoding='utf8')#输出的中文语料
	zh_cut=open('segphrase/cuts.out','r',encoding='utf8').read()#读入的中文分词结果
	print(len(zh_cut.replace(' ','')))
	pos=-1
	tot=0
	zh_out=''
	for en,zh in list_pair:
		en_txt.write(remove_punc(en.lower())+'\n')
		zh=remove_punc(zh.lower())
		for i,c in enumerate(zh):
			if is_hanzi(c):
				tot+=1
				pos+=1
				if zh_cut[pos]==' ':#如果在cuts.out中，该位置被断开，则在语料中也要被断开
					pos+=1
					zh_out+=' '
				zh_out+=c
			elif c!=' ':
				if i>0 and (is_eng(c) and not is_eng(zh[i-1])):#如果当前位置是中英文的分界处，那么也要断开
					zh_out+=' '
				zh_out+=c
				if i<len(zh)-1 and (is_eng(c) and not is_eng(zh[i+1])):#同理
					zh_out+=' '
		zh_out+='\n'
	print(tot)
	zh_txt.write(zh_out)
	zh_txt.close()
	en_txt.close()
def gizapp():#使用giza++生成词典（linux环境下）
	os.system('rm chinese.vcb chinese.vcb.classes chinese.vcb.classes.cats english.vcb \
		chinese_english.snt english_chinese.snt chn_eng.cooc')
	os.system('rm -r c2e')
	os.system('./plain2snt.out chinese english')
	os.system('./snt2cooc.out chinese.vcb english.vcb chinese_english.snt > chn_eng.cooc')
	os.system('./mkcls -pchinese -Vchinese.vcb.classes opt')
	os.system('mkdir c2e')
	os.system('./GIZA++ -S chinese.vcb -T english.vcb -C chinese_english.snt -CoocurrenceFile chn_eng.cooc -outputpath c2e')
def main2():
	#分别读取中英文单词的编号
	en_words=['','']+[x.split(' ')[1] for x in open('english.vcb','r',encoding='utf8').readlines()]
	zh_words=['','']+[x.split(' ')[1] for x in open('chinese.vcb','r',encoding='utf8').readlines()]
	prob_file=[x for x in os.listdir('c2e') if re.search('^.*\.t3\.final$',x) is not None][0]
	prob=map(lambda x:(int(x[0]),int(x[1]),float(x[2])),
		[x.strip('\n').split(' ') for x in open('c2e/'+prob_file,'r',encoding='utf8').readlines()])
	result,cur={},[0]*len(en_words)#result中保存中文词汇对应的最大概率翻译结果，cur保存最大概率的值
	for a,b,p in prob:
		if p>cur[a]:
			result[zh_words[a]]=en_words[b]
			cur[a]=p
	with open('dict.txt','w',encoding='utf8') as fp:#生成的词典文件
		for a,b in result.items():
			fp.write(a+' '+b+'\n')
	return result