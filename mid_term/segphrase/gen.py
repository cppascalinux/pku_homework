from random import choice
def readin():
	fd=open('dict.out','rt',encoding='utf-8')
	lists=fd.readlines()
	ansl=[]
	for i in range(len(lists)):
		nl=lists[i].split(' ')
		if len(nl[0])>=2 and int(nl[1])>=100:
			ansl+=[nl[0]]
	return ansl
def qry(lists):
	fout=open('train.out','wt',encoding='utf-8')
	smt,smf=0,0
	while smt<200 or smf<200:
		print('smt:',smt,"smf:",smf)
		s=choice(lists)
		ans=input(s)
		if ans!='':
			if smt<200:
				smt+=1
				print(s+' 1',file=fout)
		elif smf<200:
			smf+=1
			print(s+' 0',file=fout)
def main():
	lists=readin()
	qry(lists)
main()