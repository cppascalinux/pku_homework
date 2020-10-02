import jieba,sys
print(sys.stdout.encoding)
f1=open('第二次作业环境及要求/zbn_xinhua/xin_cmn_200010','r',encoding='utf-8')
f2=open('qwq.out','w',encoding='utf-8')
s=f1.read()
ls=jieba.lcut(s)
print(len(ls))
for i in ls:
	f2.write(i+'\n')
# print(ls)