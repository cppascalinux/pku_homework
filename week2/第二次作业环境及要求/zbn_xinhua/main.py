import os
def main():
	d=os.system
	d('time pypy3 init.py')
	if not os.path.exists('train.out'):
		d('time pypy3 gen.py')
	d('time python3 getq.py')
	d('time pypy3 pytocpp.py')
	d('g++ solve.cpp -o solve -O2')
	d('time ./solve')
	d('time pypy3 cpptopy.py')
	d('time python3 getq.py')
	d('time pypy3 pytocpp.py')
	d('time ./solve')
	d('time pypy3 cpptopy.py')
main()