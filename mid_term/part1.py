import re,os,json
zh_pre_cut=open('segphrase/input.txt','w',encoding='utf8')
def is_hanzi(s):
	return '\u4e00'<=s<='\u9fff'
def remove_punc(s):
	t=''
	punc='~`!@#$%^&*()_-+={|[]\\:";<>?,./\'}，）（！：“”；'
	for i in s:
		if not i in punc:
			t+=i
	return t
def align(en_text,zh_text,list_pair):
	en_sent=[x for x in re.split('\.',en_text.replace('\n','')) if x]
	zh_sent=[x for x in re.split('\.|。',zh_text.replace('\n','')) if x]
	if len(en_sent)!=len(zh_sent):
		return
	list_pair+=[x for x in zip(en_sent,zh_sent) if x[0]!=x[1]]
	for s in zh_sent:
		zh_pre_cut.write(remove_punc(s)+' ')
	zh_pre_cut.write('\n')
def dfs_text(dep,pos,en_text,zh_text,en_title,zh_title,en_path,zh_path,
	txt_file,num,num_full,list_pair,en_que,list_en_ans,zh_que,list_zh_ans):
	d={}
	ls=[]
	d['title']=en_title[pos][1]
	d['zh_title']=zh_title[pos][1]
	d['level']=dep
	d['code']='{:0>3d}'.format(num)
	d['content']=ls
	list_pair.append((d['title'],d['zh_title']))
	zh_pre_cut.write(remove_punc(d['zh_title'])+'\n')
	en_left_pos=en_title[pos][0][1]+1
	en_right_pos=en_title[pos+1][0][0] if pos+1<len(en_title) else len(en_text)
	zh_left_pos=zh_title[pos][0][1]+1
	zh_right_pos=zh_title[pos+1][0][0] if pos+1<len(zh_title) else len(zh_text)
	en_ans=en_text[en_left_pos:en_right_pos].strip(' \n')
	zh_ans=zh_text[zh_left_pos:zh_right_pos].strip(' \n')
	align(en_ans,zh_ans,list_pair)
	if en_ans:
		list_en_ans.append(en_ans)
		en_que.append('==>'.join(en_path))
		txt_file.write('{Q'+num_full+'En:'+'"'+'==>'.join(en_path)+'"}\n')
		txt_file.write('{A'+num_full+'En:'+'"'+en_ans+'"}\n')
	if zh_ans:
		list_zh_ans.append(zh_ans)
		zh_que.append('==>'.join(zh_path))
		txt_file.write('{Q'+num_full+'Zh:'+'"'+'==>'.join(zh_path)+'"}\n')
		txt_file.write('{A'+num_full+'Zh:'+'"'+zh_ans+'"}\n')
	next_num=0
	for i in range(pos+1,len(en_title)):
		if en_title[i][2]==en_title[pos][2]+1:
			next_num+=1
			ls.append(dfs_text(dep+1,i,en_text,zh_text,en_title,zh_title,en_path+[en_title[i][1]],zh_path+[zh_title[i][1]],
				txt_file,next_num,num_full+'{:0>3d}'.format(next_num),list_pair,en_que,list_en_ans,zh_que,list_zh_ans))
		elif en_title[i][2]<=en_title[pos][2]:
			return d
	return d
def dfs_dir(dep,path,list_path,name,txt_file,num,num_full,list_pair,en_list,en_que,list_en_ans,zh_que,list_zh_ans):
	d={}
	ls=[]
	if dep>0:
		d['title']=name
		d['zh-title']=name
		d['code']=num
	d['level']=dep
	d['content']=ls
	next_num=0
	for file_name in os.listdir(path):
		full_path=path+'/'+file_name
		if os.path.isdir(full_path):
			next_num+=1
			ls.append(dfs_dir(dep+1,full_path,list_path+[file_name],file_name,txt_file,next_num,num_full+'{:0>3d}'.format(next_num),
				list_pair,en_list,en_que,list_en_ans,zh_que,list_zh_ans))
		else:
			with open(full_path,'r',encoding='utf8') as fp:
				en_text=fp.read()
				en_list.append(en_text)
			with open(full_path.replace('python-3.9.0-docs-text-en','python-3.9.0-docs-text-zh'),'r',encoding='utf8') as fp:
				zh_text=fp.read()
			en_title_1=[(x.span(),x.group().strip('1234567890.* \n'),1) for x in re.finditer(r'^.+\n.\*+$',en_text,flags=re.MULTILINE)]
			en_title_2=[(x.span(),x.group().strip('1234567890.= \n'),2) for x in re.finditer(r'^.+\n.=+$',en_text,flags=re.MULTILINE)]
			en_title_3=[(x.span(),x.group().strip('1234567890.- \n'),3) for x in re.finditer(r'^.+\n.-+$',en_text,flags=re.MULTILINE)]
			zh_title_1=[(x.span(),x.group().strip('1234567890.* \n'),1) for x in re.finditer(r'^.+\n.\*+$',zh_text,flags=re.MULTILINE)]
			zh_title_2=[(x.span(),x.group().strip('1234567890.= \n'),2) for x in re.finditer(r'^.+\n.=+$',zh_text,flags=re.MULTILINE)]
			zh_title_3=[(x.span(),x.group().strip('1234567890.- \n'),3) for x in re.finditer(r'^.+\n.-+$',zh_text,flags=re.MULTILINE)]
			en_title_all=sorted(en_title_1+en_title_2+en_title_3,key=lambda x:x[0][0])
			zh_title_all=sorted(zh_title_1+zh_title_2+zh_title_3,key=lambda x:x[0][0])
			if en_title_all:
				next_num+=1
				ls.append(dfs_text(dep+1,0,en_text,zh_text,en_title_all,zh_title_all,
					list_path+[en_title_all[0][1]],list_path+[zh_title_all[0][1]],
					txt_file,next_num,num_full+'{:0>3d}'.format(next_num),list_pair,en_que,list_en_ans,zh_que,list_zh_ans))
	return d
def main():
	en_path='python-3.9.0-docs-text-en'
	zh_path='python-3.9.0-docs-text-zh'
	list_pair=[]
	en_list=[]
	en_que,list_en_ans,zh_que,list_zh_ans=[],[],[],[]
	txt_file=open('output.txt','w',encoding='utf8')
	d=dfs_dir(0,en_path,[],'',txt_file,0,'',list_pair,en_list,en_que,list_en_ans,zh_que,list_zh_ans)
	json_file=open('output.json','w',encoding='utf8')
	str_json=json.dumps(d,indent='\t',ensure_ascii=False)
	json_file.write(str_json)
	en_all='\n'.join(en_list)
	zh_pre_cut.close()
	return list_pair,en_all,en_que,list_en_ans,zh_que,list_zh_ans
