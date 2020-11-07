"pipes" --- 终端管道接口
************************

**源代码：** Lib/pipes.py

======================================================================

"pipes" 定义了一个类用来抽象 *pipeline* 的概念 --- 将数据从一个文件转
到另一文件的转换器序列。

由于模块使用了 **/bin/sh** 命令行，因此要求有 POSIX 或兼容
"os.system()" 和 "os.popen()" 的终端程序。

"pipes" 模块定义了以下的类:

class pipes.Template

   对管道的抽象。

示例:

   >>> import pipes
   >>> t = pipes.Template()
   >>> t.append('tr a-z A-Z', '--')
   >>> f = t.open('pipefile', 'w')
   >>> f.write('hello world')
   >>> f.close()
   >>> open('pipefile').read()
   'HELLO WORLD'


模板对象
========

模板对象有以下方法:

Template.reset()

   将一个管道模板恢复为初始状态。

Template.clone()

   返回一个新的等价的管道模板。

Template.debug(flag)

   如果 *flag* 为真值，则启用调试。 否则禁用调试。 当启用调试时，要执
   行的命令会被打印出来，并且会给予终端 "set -x" 命令以输出更详细的信
   息。

Template.append(cmd, kind)

   在末尾添加一个新的动作。 *cmd* 变量必须为一个有效的 bourne 终端命令
   。 *kind* 变量由两个字母组成。

   第一个字母可以为 "'-'" (这表示命令将读取其标准输入), "'f'" (这表示
   命令将读取在命令行中给定的文件) 或 "'.'" (这表示命令将不读取输入，
   因而必须放在前面。)

   类似地，第二个字母可以为 "'-'" (这表示命令将写入到标准输出), "'f'"
   (这表示命令将写入在命令行中给定的文件) 或 "'.'" (这表示命令将不执行
   写入，因而必须放在末尾。)

Template.prepend(cmd, kind)

   在开头添加一个新的动作。 请参阅 "append()" 获取相应参数的说明。

Template.open(file, mode)

   返回一个文件类对象，打开到 *file*，但是将从管道读取或写入。 请注意
   只能给出 "'r'", "'w'" 中的一个。

Template.copy(infile, outfile)

   通过管道将 *infile* 拷贝到 *outfile*。
