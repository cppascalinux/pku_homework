import gc
def main():
	sin=open('cuts_cpp.out','rt',encoding='utf-8')
	win=open('words_cpp.out','rt',encoding='utf-8')
	fin=open('features_cpp.out','rt',encoding='utf-8')
	lin=open('label.out','rt',encoding='utf-8')
	din=open('dict.out','rt',encoding='utf-8')
	sout=open('cuts.out','wt',encoding='utf-8')
	wout=open('words.out','wt',encoding='utf-8')
	l=[x.split(' ')[1][:-1] for x in lin.readlines()]
	l[0]=' '
	lists=[l[int(x)] for x in sin.read().split(' ') if x!='']
	for wd in lists:
		sout.write(wd)
	lists=[x.split(' ') for x in win.readlines()]
	for ls in lists:
		ts=''
		for v in ls[:-1]:
			ts+=l[int(v)]
		if len(ts)>1 and ls[-1]!='0\n':
			wout.write(ts+' '+ls[-1])
	gc.collect()
	lists=[x for x in fin.readlines()]
	listd=din.readlines()
	din.close();
	dout=open('dict.out','wt',encoding='utf-8')
	n=len(lists)
	for i in range(n):
		dout.write(listd[i][:-1]+lists[i])
main()