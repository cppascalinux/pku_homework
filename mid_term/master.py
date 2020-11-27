import part1,part2,part3,part4,part6,os
list_pair,en_all,en_que,en_ans,zh_que,zh_ans=part1.main()
if not os.path.exists('segphrase/cuts.out'):
	print('111')
	os.system('cd segphrase;python main.py')
part2.main1(list_pair)
if not os.path.exists('c2e'):
	print('222')
	part2.gizapp()
dic=part2.main2()
mat=part3.main(en_all)
a=part6.InteractGUI(dic,mat,en_que,en_ans,zh_que,zh_ans)
a.start()