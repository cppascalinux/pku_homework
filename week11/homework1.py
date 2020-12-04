# 先把要复制的文件放在current文件夹下

import os, shutil, time
from multiprocessing import Pool, Manager
tot=0

# 定义了一个copy文件的方法
def copy_file(q, num, file, old_folder, new_folder):
    # while not q.empty():
    # file=q.get()
    source = os.path.join(old_folder, file)
    target = os.path.join(new_folder, file)

    file_size = (os.path.getsize(old_folder + "/" + file)) / 1024 / 1024
    cur=q.get()
    q.put(cur+1)
    blocks=int(cur/tot*50)
    print("[%s] %d%% id:%d Size：%.2f M | %s" % ('#'*blocks+'.'*(50-blocks), int(cur/tot*100), num, file_size, target),end='\r')
    with open(source, "rb") as fr:
        with open(target, "wb") as fw:
            while True:
                content = fr.read(1024 * 1024)
                fw.write(content)
                if not content:
                    break

def main():
    current_folder = './current'
    target_folder = './target'

    if os.path.exists(target_folder):
        shutil.rmtree(target_folder)

    os.mkdir(target_folder)

    # 获取当前目录下所有的文件名
    all_file = os.listdir(current_folder)
    global tot
    tot=len(all_file)
    start=time.time()
    cores=16
    pl=Pool(cores)
    q=Manager().Queue()
    q.put(1)
    # for file in all_file:
    #     q.put(file)
    for i,file in enumerate(all_file):
        pl.apply_async(copy_file,args=(q,i+1,file,current_folder,target_folder))
    pl.close()
    pl.join()
    # 复制
    # for file in all_file:
    #     copy_file(0, file, current_folder, target_folder)
    end=time.time()
    print(f'\nfinished,time:{end-start}s')
if __name__ == '__main__':
    main()
