import os
def main():
	d=os.system
	d('python init.py')
	if not os.path.exists('train.out'):
		d('pypy3 gen.py')
	d('python getq.py')
	d('pypy3 pytocpp.py')
	d('g++ solve.cpp -o solve -O2')
	d('solve')
	d('pypy3 cpptopy.py')
	d('python getq.py')
	d('pypy3 pytocpp.py')
	d('solve')
	d('pypy3 cpptopy.py')
main()