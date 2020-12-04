import os,shutil
def main():
	current_folder='./current'
	target_folder='./target'
	if os.path.exists(current_folder):
		shutil.rmtree(current_folder)
	os.mkdir(current_folder)
	for i in range(3000):
		file=current_folder+f'/{i}.txt'
		with open(file,'wb') as fp:
			fp.write(('0'*10*1048576).encode('utf8'))
main()