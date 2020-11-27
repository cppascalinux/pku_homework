import tkinter as tk
import tkinter.scrolledtext as tkst#可滚动文本框
import part4,part5,re
# def main(dic,mat,en_que,en_ans,zh_que,zh_ans):
class InteractGUI:
	def __init__(self,dic,mat,en_que,en_ans,zh_que,zh_ans):#主要是构建了页面左侧的控件
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
		self.fm_left=tk.Frame(self.root)#左侧框架
		self.fm_left.place(x=0,y=0,width=500,height=800)#使用place放置
		self.fm_right=tk.Frame(self.root)#右侧框架
		self.fm_right.place(x=500,y=0,width=900,height=800)#使用place放置
		tk.Label(self.fm_left).pack(fill='x',pady=50)#pack放置一个空标签用于占位
		self.lb_que=tk.Label(self.fm_left,text='请输入查询内容(支持中英文)')#标签
		self.lb_que.pack(fill='x',pady=10)
		self.input_et=tk.Entry(self.fm_left)#输入框
		self.input_et.pack(fill='x',pady=10)
		use_re=tk.IntVar()#是否使用正则表达式
		self.chk_box=tk.Checkbutton(self.fm_left,text='使用*?通配符(仅限英文查询)',variable=use_re)#复选框
		self.chk_box.pack(fill='x',pady=10)
		self.button_search=tk.Button(self.fm_left,text='搜索!',#搜索按钮
			command=lambda:(self.search(self.input_et.get(),use_re.get()),self.show_trans(self.input_et.get())))
		self.button_search.pack(fill='x',pady=10)
		self.button_clear=tk.Button(self.fm_left,text='清空输出框',command=self.clear)#清空输出框的按钮
		self.button_clear.pack(fill='x',pady=10)
		self.lb_trans=tk.Label(self.fm_left,text='翻译结果:')
		self.lb_trans.pack(fill='x',pady=10)
		self.text_trans=tk.Text(self.fm_left)#显示翻译结果的文本框
		self.text_trans.pack(fill='both',pady=10)
	def show_trans(self,zh_text):#显示翻译结果
		self.text_trans.delete('1.0','end')
		if part5.is_chinese(zh_text):
			en_text=part4.main(zh_text,self.dic,self.mat)
			self.text_trans.insert('end',en_text)
	def start(self):#启动窗口
		self.root.mainloop()
	def search(self,str_input,use_re):#查询的函数
		list_qa=part5.main(str_input,self.dic,self.mat,self.en_que,self.en_ans,self.zh_que,self.zh_ans,use_re)
		self.show_que(list_qa)
	def clear(self,all=True):#清空结果
		for widget in self.fm_right.winfo_children():
			widget.destroy()
		if all:#是否清空翻译框
			self.text_trans.delete('1.0','end')
	def show_ans(self,s):#显示对应的回答
		self.clear(False)
		self.text=tkst.ScrolledText(self.fm_right)#可滚动文本框
		self.text.pack(fill='both',expand=True)
		self.text.insert(tk.END,s)
	def show_que(self,list_qa):#显示所有匹配的问题
		self.clear()
		self.scroll=tk.Scrollbar(self.fm_right)#滚动条
		self.canvas=tk.Canvas(self.fm_right)#生成一个canvas，用于作为可滚动Frame的父控件
		self.canvas.config(yscrollcommand=self.scroll.set)
		self.scroll.pack(side='right',fill='y')
		self.canvas.pack(side='left',fill='both',expand=True)
		self.fm_buttons=tk.Frame(self.canvas)#在Canvas上新建一个Frame
		#在Frame的尺寸发生变化的时候，便将canvas的可滚动区域改变为它的大小，这样保证所有的区域都是可滚动的
		self.fm_buttons.bind('<Configure>',lambda e:self.canvas.config(scrollregion=self.canvas.bbox('all')))
		self.scroll.config(command=self.canvas.yview)
		def deco(s):#一个闭包。。用于生成按钮command需要的函数
			return lambda:self.show_ans(s)
		for q,a in list_qa:#生成所有按钮
			nbutton=tk.Button(self.fm_buttons,text=q,command=deco(q+'\n'+a))
			nbutton.pack(fill='x')
		self.canvas.create_window((0,0),window=self.fm_buttons,anchor='nw',width=890)#在canvas上绘制Frame