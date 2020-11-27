import re,json
def main(en_all):
	mat,sum_rep={},{}
	# print(en_all)
	ls_sent=[x[1] for x in re.findall('( |\n)([A-Z][A-Za-z0-9\* ,:;\'"\n]*[\.!\?])( |\n)',en_all)]
	for s in ls_sent:
		ls_words=[x for x in re.split('[^a-z]',s.lower()) if x]
		l=len(ls_words)
		for i in range(l+1):
			wd_pre=ls_words[i-1] if i>0 else 'BOS'
			wd_cur=ls_words[i] if i<l else 'EOS'
			if not wd_pre in mat:
				mat[wd_pre]={}
				sum_rep[wd_pre]=0
			if not wd_cur in mat[wd_pre]:
				mat[wd_pre][wd_cur]=0
			mat[wd_pre][wd_cur]+=1
			sum_rep[wd_pre]+=1
	for wd_pre in mat:
		for wd_cur in mat[wd_pre]:
			mat[wd_pre][wd_cur]/=sum_rep[wd_pre]
	print(len(mat))
	# mat_json=json.dumps(mat,indent='\t',ensure_ascii=False)
	# with open('mat.json','w',encoding='utf8') as fp:
	# 	fp.write(mat_json)
	return mat
	# with open('part3.txt','w',encoding='utf8') as fp:
	# 	fp.write(str(ls_sent))
		# fp.write(en_all)
	# print(ls_sent)
