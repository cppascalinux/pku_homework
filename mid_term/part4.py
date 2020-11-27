import jieba,math
R=0.85#平滑因子
K=10000#每层BFS保留状态数量
def get_prob(wd_pre,wd_cur,mat):#计算wd_pre转移到wd_cur的概率
	if wd_pre in mat:
		if wd_cur in mat[wd_pre]:
			return math.log(R*mat[wd_pre][wd_cur]+(1-R)/len(mat))#有R的概率依照矩阵转移，（1-r）的概率随机转移
	return math.log((1-R)/len(mat))
def bfs(en_ls,mat):#保留前K大的BFS
	ls=[]
	n=len(en_ls)
	for i in range(K):
		ls.append([['BOS'],0,[-1]])#以BOS作为起始
	for i in range(n):
		next_ls=[]
		for j in range(K):
			for k,wd in enumerate(en_ls):
				if k not in ls[j][2]:
					next_ls.append([ls[j][0]+[wd],ls[j][1]+get_prob(ls[j][0][-1],wd,mat),ls[j][2]+[k]])
		ls=sorted(next_ls,key=lambda x:x[1],reverse=True)[:K]#选取前K大
	return ' '.join(sorted(ls,key=lambda x:x[1]+get_prob(x[0][-1],'EOS',mat),reverse=True)[0][0][1:])#选取最终概率最大的序列
def main(zh_input,dic,mat):
	punc='~`!@#$%^&*()_-+={|[]\\:";<>?,./\'}，。）（！：；“”‘’'
	zh_ls=[x for x in jieba.lcut(zh_input.lower()) if x not in punc]#使用jieba对输入的中文句子分词，并得到对应的英文词袋
	en_ls=[dic[x] for x in zh_ls if x in dic]
	return bfs(en_ls,mat)