import re,part4
def is_chinese(s):#判断一个字符串是否存在汉字
	for c in s:
		if '\u4e00'<=c<='\u9fff':
			return True
	return False
def build_re(s,use_re):
	if use_re:#表示使用*?作为通配符
		punc='.+$^[]}{()|\\'#在正则表达式模式串中需要转义的字符
	else:#不使用通配符
		punc='.+$^[]}{()|\\?*'
	t=''#生成的模式串
	for c in s:
		if c in punc:#需要转义
			t+='\\'+c
		elif c=='?':#通配符
			t+='.?'
		elif c=='*':#通配符
			t+='.*'
		else:#直接添加该字符
			t+=c
	return t
def main(str_input,dic,mat,en_que,en_ans,zh_que,zh_ans,use_re):
	str_pat=build_re(str_input,use_re)#构建模式串
	ls_output=[]#保存所有匹配的问题与对应的回答
	if not is_chinese(str_input):#如果输入的串是纯英文串
		for i in range(len(en_ans)):
			sq,sa=en_que[i],en_ans[i]
			if re.search(str_pat,(sq+sa).replace('\n',''),flags=re.IGNORECASE) is not None:
				ls_output.append((sq,sa))
	else:#输入的串中含有中文
		for i in range(len(zh_ans)):
			sq,sa=zh_que[i],zh_ans[i]
			if re.search(str_pat,(sq+sa).replace('\n',''),flags=re.IGNORECASE) is not None:
				ls_output.append((sq,sa))
		str_en=part4.main(str_input,dic,mat)#将该串翻译成中文
		if str_en:
			for i in range(len(en_ans)):
				sq,sa=en_que[i],en_ans[i]
				if re.search(str_en,(sq+sa).replace('\n',''),flags=re.IGNORECASE) is not None:
					ls_output.append((sq,sa))
	return ls_output