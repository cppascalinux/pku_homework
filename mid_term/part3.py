import re,json
def main(en_all):#计算词转移概率矩阵
	mat,sum_rep={},{}#分别保存词转移次数，和某个词的后继总数
	#使用re匹配所有合法的英文句子：前面有空格或者回车，第一个字母大写，句子由字母和数字，标点等组成，并以'.'结尾，同时后面仍存在空格或回车
	ls_sent=[x[1] for x in re.findall('( |\n)([A-Z][A-Za-z0-9\* ,:;\'"\n]*[\.!\?])( |\n)',en_all)]
	for s in ls_sent:
		ls_words=[x for x in re.split('[^a-z]',s.lower()) if x]#在所有非字母位置切分
		l=len(ls_words)
		for i in range(l+1):
			#考虑BOS和EOS
			wd_pre=ls_words[i-1] if i>0 else 'BOS'
			wd_cur=ls_words[i] if i<l else 'EOS'
			if not wd_pre in mat:
				mat[wd_pre]={}
				sum_rep[wd_pre]=0
			if not wd_cur in mat[wd_pre]:
				mat[wd_pre][wd_cur]=0
			mat[wd_pre][wd_cur]+=1#转移次数+1
			sum_rep[wd_pre]+=1#总转移次数
	for wd_pre in mat:
		for wd_cur in mat[wd_pre]:
			mat[wd_pre][wd_cur]/=sum_rep[wd_pre]#计算转移概率
	print(len(mat))
	return mat
