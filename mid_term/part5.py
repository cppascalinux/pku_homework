import re,part4
def is_chinese(s):
	for c in s:
		if '\u4e00'<=c<='\u9fa5':
			return True
	return False
def build_re(s,use_re):
	if use_re:
		punc='.+$^[]}{()|\\'
	else:
		punc='.+$^[]}{()|\\?*'
	t=''
	for c in s:
		if c in punc:
			t+='\\'+c
		elif c=='?':
			t+='.?'
		elif c=='*':
			t+='.*'
		else:
			t+=c
	return t
def main(str_input,dic,mat,en_que,en_ans,zh_que,zh_ans,use_re):
	str_pat=build_re(str_input,use_re)
	ls_output=[]
	if not is_chinese(str_input):
		for i in range(len(en_ans)):
			sq,sa=en_que[i],en_ans[i]
			if re.search(str_pat,sq+'\n'+sa,flags=re.IGNORECASE) is not None:
				ls_output.append((sq,sa))
	else:
		for i in range(len(zh_ans)):
			sq,sa=zh_que[i],zh_ans[i]
			if re.search(str_pat,sq+'\n'+sa,flags=re.IGNORECASE) is not None:
				ls_output.append((sq,sa))
		str_en=part4.main(str_input,dic,mat)
		for i in range(len(en_ans)):
			sq,sa=en_que[i],en_ans[i]
			if re.search(str_en,sq+'\n'+sa,flags=re.IGNORECASE) is not None:
				ls_output.append((sq,sa))
	return ls_output