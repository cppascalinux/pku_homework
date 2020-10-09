def main():
	n=1000
	xin=open('words_xin.out','rt',encoding='utf-8')
	zin=open('words_zbn.out','rt',encoding='utf-8')
	lx=[x.split(' ')[0] for x in xin.readlines()[:n]]
	lz=[x.split(' ')[0] for x in zin.readlines()[:n]]
	sx=set(lx)
	sz=set(lz)
	ox,oz,oxz=[],[],[]
	for s in lx:
		if s in sz:
			oxz+=[s]
		else:
			ox+=[s]
	for s in lz:
		if not s in sx:
			oz+=[s] 
	xout=open('words_xin_only.out','wt',encoding='utf-8')
	zout=open('words_zbn_only.out','wt',encoding='utf-8')
	xzout=open('words_both.out','wt',encoding='utf-8')
	for s in ox:
		xout.write(s+'\n')
	for s in oz:
		zout.write(s+'\n')
	for s in oxz:
		xzout.write(s+'\n')
main()