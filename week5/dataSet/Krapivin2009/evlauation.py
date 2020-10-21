import os

def getWordsFromFile(filePath):
    res=[]
    file=open(filePath)
    for line in file.readlines():
        line=line.strip('\n')
        res.append(line)
    file.close()
    return res

def getFileNamesFromFolder(folderPath,fileType):
    '''
    :param folderPath: the path of your folder
    :param fileType: the postfix,such as ".txt"
    :return: stringList of file
    '''
    L=[]
    for root, dirs, files in os.walk(folderPath):
      for file in files:
        if os.path.splitext(file)[1] == fileType:
          L.append(os.path.join(root, file))
    return L
# os.walk返回一个三元组(root,dirs,files)
# root 所指的是当前正在遍历的这个文件夹的本身的地址
# dirs 是一个 list ，内容是该文件夹中所有的目录的名字(不包括子目录)
# files 同样是 list , 内容是该文件夹中所有的文件(不包括子目录)
# 其中os.path.splitext()函数将路径拆分为文件名+扩展名

def evaluateOneArticle(outputFile,groundTruthFile):
    res={}
    output=getWordsFromFile(outputFile)
    groundTruth=getWordsFromFile(groundTruthFile)
    gt_cnt=len(groundTruth)
    out_cnt=len(output)
    good_cnt=len(set(output) & set(groundTruth))
    res['p'] = 1.0 * good_cnt / out_cnt
    res['r'] = 1.0 * good_cnt / gt_cnt
    res['f'] = 2.0 * res['p'] * res['r'] / (res['p'] + res['r'])
    return res

def evaluateAll(folderPath):
    res={}
    res['p']=0.0
    res['r']=0.0
    res['f']=0.0
    gtFiles=getFileNamesFromFolder(folderPath,".key")
    myFiles=getFileNamesFromFolder(folderPath,".mykey")
    assert (len(gtFiles)==len(myFiles))
    for file in gtFiles:
        fileName=os.path.splitext(file)[0]
        res_=evaluateOneArticle(fileName+".mykey",fileName+".key")
        res['p']+=res_['p']
        res['r'] += res_['r']
        res['f'] += res_['f']
    res['p']/=len(gtFiles)
    res['r']/=len(gtFiles)
    res['f']/=len(gtFiles)
    return res

if __name__== '__main__':
    print(evaluateAll(".\\testModule"))