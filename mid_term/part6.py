import tkinter as tk
import tkinter.scrolledtext as tkst
import part4,part5,re
# def main(dic,mat,en_que,en_ans,zh_que,zh_ans):
class InteractGUI:
	def __init__(self,dic,mat,en_que,en_ans,zh_que,zh_ans):
	# def __init__(self):
		self.dic=dic
		self.mat=mat
		self.dic=dic
		self.en_que=en_que
		self.en_ans=en_ans
		self.zh_que=zh_que
		self.zh_ans=zh_ans
		self.root=tk.Tk()
		self.root.geometry('1400x800+200+100')
		self.root.title('Python文档自助查询系统')
		self.fm_left=tk.Frame(self.root)
		self.fm_left.place(x=0,y=0,width=500,height=800)
		self.fm_right=tk.Frame(self.root)
		self.fm_right.place(x=500,y=0,width=900,height=800)
		tk.Label(self.fm_left).pack(fill='x',pady=50)
		self.lb_que=tk.Label(self.fm_left,text='请输入查询内容(支持中英文)')
		self.lb_que.pack(fill='x',pady=10)
		self.input_et=tk.Entry(self.fm_left)
		self.input_et.pack(fill='x',pady=10)
		use_re=tk.IntVar()
		self.chk_box=tk.Checkbutton(self.fm_left,text='使用*?通配符(仅限英文查询)',variable=use_re)
		self.chk_box.pack(fill='x',pady=10)
		self.button_search=tk.Button(self.fm_left,text='搜索!',
			command=lambda:(self.search(self.input_et.get(),use_re.get()),self.show_trans(self.input_et.get())))
		self.button_search.pack(fill='x',pady=10)
		self.button_clear=tk.Button(self.fm_left,text='清空输出框',command=self.clear)
		self.button_clear.pack(fill='x',pady=10)
		self.lb_trans=tk.Label(self.fm_left,text='翻译结果:')
		self.lb_trans.pack(fill='x',pady=10)
		self.text_trans=tk.Text(self.fm_left)
		self.text_trans.pack(fill='both',pady=10)
	def show_trans(self,zh_text):
		self.text_trans.delete('1.0','end')
		if part5.is_chinese(zh_text):
			en_text=part4.main(zh_text,self.dic,self.mat)
			self.text_trans.insert('end',en_text)
	def start(self):
		self.root.mainloop()
	def search(self,str_input,use_re):
		list_qa=part5.main(str_input,self.dic,self.mat,self.en_que,self.en_ans,self.zh_que,self.zh_ans,use_re)
		self.show_que(list_qa)
	def clear(self):
		for widget in self.fm_right.winfo_children():
			widget.destroy()
	def show_ans(self,s):
		self.clear()
		self.text=tkst.ScrolledText(self.fm_right)
		self.text.pack(fill='both',expand=True)
		self.text.insert(tk.END,s)
	def show_que(self,list_qa):
		self.clear()
		self.scroll=tk.Scrollbar(self.fm_right)
		self.canvas=tk.Canvas(self.fm_right)
		self.canvas.config(yscrollcommand=self.scroll.set)
		self.scroll.pack(side='right',fill='y')
		self.canvas.pack(side='left',fill='both',expand=True)
		self.fm_buttons=tk.Frame(self.canvas)
		self.fm_buttons.bind('<Configure>',lambda e:self.canvas.config(scrollregion=self.canvas.bbox('all')))
		self.scroll.config(command=self.canvas.yview)
		def deco(s):
			return lambda:self.show_ans(s)
		for q,a in list_qa:
			nbutton=tk.Button(self.fm_buttons,text=q,command=deco(q+'\n'+a))
			nbutton.pack(fill='x')
		self.canvas.create_window((0,0),window=self.fm_buttons,anchor='nw',width=890)
		# self.fm_buttons.pack(fill='both')
		# self.canvas.create_window()
		# print(self.fm_buttons.bbox('all'))
		# print(self.canvas.bbox('all'))
# def main():
# 	# a=InteractGUI()
# 	# ls=[]
# 	# for i in range(1000):
# 	# 	ls.append((str(i),str(i)))
# 	# a.show_que(ls)
# 	a.start()
# main()