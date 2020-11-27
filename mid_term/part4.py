import jieba,math
R=0.9
K=10000
def get_prob(wd_pre,wd_cur,mat):
	# if wd_pre=='BOE':
	# 	return 0
	if wd_pre in mat:
		if wd_cur in mat[wd_pre]:
			return math.log(R*mat[wd_pre][wd_cur]+(1-R)/len(mat))
	return math.log((1-R)/len(mat))
def bfs(en_ls,mat):
	# print(en_ls)
	ls=[]
	n=len(en_ls)
	for i in range(K):
		ls.append([['BOS'],0,[-1]])
	for i in range(n):
		# print(i)
		next_ls=[]
		for j in range(K):
			# print('j:',j)
			for k,wd in enumerate(en_ls):
				if k not in ls[j][2]:
					next_ls.append([ls[j][0]+[wd],ls[j][1]+get_prob(ls[j][0][-1],wd,mat),ls[j][2]+[k]])
		ls=sorted(next_ls,key=lambda x:x[1],reverse=True)[:K]
	return ' '.join(sorted(ls,key=lambda x:x[1]+get_prob(x[0][-1],'EOS',mat),reverse=True)[0][0][1:])
	# return ' '.join(ls[0][0][1:])
	# return ' '.join(en_ls)
def main(zh_input,dic,mat):
	punc='~`!@#$%^&*()_-+={|[]\\:";<>?,./\'}，。）（！：'
	zh_ls=[x for x in jieba.lcut(zh_input.lower()) if x not in punc]
	en_ls=[dic[x] for x in zh_ls if x in dic]
	return bfs(en_ls,mat)