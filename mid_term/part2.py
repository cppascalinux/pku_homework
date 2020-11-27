import jieba,os,re
def remove_punc(s):
	t=''
	punc='~`!@#$%^&*()_-+={|[]\\:";<>?,./\'}，）（！：“”；'
	for i in s:
		if not i in punc:
			t+=i
	return t
def is_hanzi(s):
	return '\u4e00'<=s<='\u9fff'
def is_eng(s):
	return 'a'<=s<='z' or 'A'<=s<='Z'
def main1(list_pair):
	en_txt=open('english','w',encoding='utf8')
	zh_txt=open('chinese','w',encoding='utf8')
	zh_cut=open('segphrase/cuts.out','r',encoding='utf8').read()
	print(len(zh_cut.replace(' ','')))
	# zh_pre_cut=open('segphrase/input.txt','w',encoding='utf8')
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
				if zh_cut[pos]==' ':
					pos+=1
					zh_out+=' '
				zh_out+=c
			elif c!=' ':
				if i>0 and (is_eng(c) and not is_eng(zh[i-1])):
					zh_out+=' '
				zh_out+=c
				if i<len(zh)-1 and (is_eng(c) and not is_eng(zh[i+1])):
					zh_out+=' '
		zh_out+='\n'
	print(tot)
	zh_txt.write(zh_out)
		# zh_txt.write(remove_punc(' '.join(jieba.lcut(zh))).lower()+'\n')
		# zh_hans=remove_punc(zh)
		# zh_pre_cut.write(zh_hans+' ')
	zh_txt.close()
	en_txt.close()
def gizapp():
	os.system('rm chinese.vcb chinese.vcb.classes chinese.vcb.classes.cats english.vcb \
		chinese_english.snt english_chinese.snt chn_eng.cooc')
	os.system('rm -r c2e')
	os.system('./plain2snt.out chinese english')
	os.system('./snt2cooc.out chinese.vcb english.vcb chinese_english.snt > chn_eng.cooc')
	os.system('./mkcls -pchinese -Vchinese.vcb.classes opt')
	os.system('mkdir c2e')
	os.system('./GIZA++ -S chinese.vcb -T english.vcb -C chinese_english.snt -CoocurrenceFile chn_eng.cooc -outputpath c2e')
def main2():
	en_words=['','']+[x.split(' ')[1] for x in open('english.vcb','r',encoding='utf8').readlines()]
	zh_words=['','']+[x.split(' ')[1] for x in open('chinese.vcb','r',encoding='utf8').readlines()]
	# print(os.listdir('c2e'))
	prob_file=[x for x in os.listdir('c2e') if re.search('^.*\.t3\.final$',x) is not None][0]
	prob=map(lambda x:(int(x[0]),int(x[1]),float(x[2])),
		[x.strip('\n').split(' ') for x in open('c2e/'+prob_file,'r',encoding='utf8').readlines()])
	result,cur={},[0]*len(en_words)
	for a,b,p in prob:
		if p>cur[a]:
			result[zh_words[a]]=en_words[b]
			cur[a]=p
	with open('dict.txt','w',encoding='utf8') as fp:
		for a,b in result.items():
			fp.write(a+' '+b+'\n')
	return result
# main1()
# main2()