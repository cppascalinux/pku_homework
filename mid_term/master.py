import part1,part2,part3,part4,part6,os
list_pair,en_all,en_que,en_ans,zh_que,zh_ans=part1.main()#第一部分
if not os.path.exists('segphrase/cuts.out'):#尚未完成分词
	os.system('cd segphrase;python main.py')#进行分词
part2.main1(list_pair)#对中英文语料进行句对齐
if not os.path.exists('c2e'):#尚未使用giza++计算词典
	part2.gizapp()
dic=part2.main2()#处理得到词典
mat=part3.main(en_all)#计算词转移概率矩阵
a=part6.InteractGUI(dic,mat,en_que,en_ans,zh_que,zh_ans)#生成一个GUI实例
a.start()#启动窗口