"cmd" --- 支持面向行的命令解释器
********************************

**源代码:** Lib/cmd.py

======================================================================

"Cmd" 类提供简单框架用于编写面向行的命令解释器。  这些通常对测试工具，
管理工具和原型有用，这些工具随后将被包含在更复杂的接口中。

class cmd.Cmd(completekey='tab', stdin=None, stdout=None)

   一个 "Cmd" 实例或子类实例是面向行的解释器框架结构。 实例化 "Cmd" 本
   身是没有充分理由的， 它作为自定义解释器类的超类是非常有用的为了继承
   "Cmd" 的方法并且封装动作方法。

   可选参数 *completekey* 是完成键的 "readline" 名称；默认是 "Tab" 。
   如果 *completekey* 不是 "None" 并且 "readline" 是可用的， 命令完成
   会自动完成。

   可选参数 *stdin* 和 *stdout* 指定了Cmd实例或子类实例将用于输入和输
   出的输入和输出文件对象。如果没有指定，他们将默认为 "sys.stdin" 和
   "sys.stdout" 。

   如果你想要使用一个给定的 *stdin* ，确保将实例的 "use_rawinput" 属性
   设置为 "False" ，否则 *stdin* 将被忽略。


Cmd 对象
========

"Cmd" 实例有下列方法：

Cmd.cmdloop(intro=None)

   反复发出提示，接受输入，从收到的输入中解析出一个初始前缀，并分派给
   操作方法，将其余的行作为参数传递给它们。

   可选参数是在第一个提示之前发布的横幅或介绍字符串（这将覆盖 "intro"
   类属性）。

   如果 "readline" 继承模块被加载，输入将自动继承类似 **bash**的历史列
   表编辑（例如， "Control-P" 滚动回到最后一个命令， "Control-N" 转到
   下一个命令，以 "Control-F" 非破坏性的方式向右 "Control-B" 移动光标
   ，破坏性地等）。

   输入的文件结束符被作为字符串传回 "'EOF'" 。

   解释器实例将会识别命令名称 "foo" 当且仅当它有方法 "do_foo()" 。有一
   个特殊情况，分派始于字符 "'?'" 的行到方法 "do_help()" 。另一种特殊
   情况，分派始于字符 "'!'" 的行到方法 "do_shell()" （如果定义了这个方
   法）

   这个方法将返回当 "postcmd()" 方法返回一个真值 。参数 *stop* 到
   "postcmd()" 是命令对应的返回值 "do_*()" 的方法。

   如果激活了完成，全部命令将会自动完成，并且通过调用 "complete_foo()"
   参数 *text* , *line*, *begidx* ,和 *endidx* 完成全部命令参数。
   *text* 是我们试图匹配的字符串前缀，所有返回的匹配项必须以它为开头。
   *line* 是删除了前导空格的当前的输入行， *begidx* 和 *endidx* 是前缀
   文本的开始和结束索引。，可以用于根据参数位置提供不同的完成。

   所有 "Cmd" 的子类继承一个预定义 "do_help()" 。 这个方法使用参数
   "'bar'" 调用， 调用对应的方法 "help_bar()" ，如果不存在，打印
   "do_bar()" 的文档字符串，如果可用。没有参数的情况下， "do_help()"
   方法会列出所有可用的帮助主题 （即所有具有相应的 "help_*()" 方法或命
   令的 文档字符串），也会列举所有未被记录的命令。

Cmd.onecmd(str)

   解释该参数，就好像它是为响应提示而键入的一样。 这可能会被覆盖，但通
   常不应该被覆盖; 请参阅： "precmd()" 和 "postcmd()" 方法，用于执行有
   用的挂钩。 返回值是一个标志，指示解释器对命令的解释是否应该停止。
   如果命令 *str* 有一个 "do_*()" 方法，则返回该方法的返回值，否则返回
   "default()" 方法的返回值。

Cmd.emptyline()

   在响应提示输入空行时调用的方法。如果此方法未被覆盖，则重复输入的最
   后一个非空命令。

Cmd.default(line)

   当命令前缀不能被识别的时候在输入行调用的方法。如果此方法未被覆盖，
   它将输出一个错误信息并返回。

Cmd.completedefault(text, line, begidx, endidx)

   当没有特定于命令的 "complete_*()" 方法可用时，调用此方法完成输入行
   。默认情况下，它返回一个空列表。

Cmd.precmd(line)

   钩方法在命令行 *line* 被解释之前执行，但是在输入提示被生成和发出后
   。这个方法是一个在 "Cmd" 中的存根；它的存在是为了被子类覆盖。返回值
   被用作  "onecmd()" 方法执行的命令； "precmd()" 的实现或许会重写命令
   或者简单的返回 *line* 不变。

Cmd.postcmd(stop, line)

   钩方法只在命令调度完成后执行。这个方法是一个在 "Cmd" 中的存根；它的
   存在是为了子类被覆盖。 *line* 是被执行的命令行， *stop* 是一个表示
   在调用 "postcmd()" 之后是否终止执行的标志；这将作为 "onecmd()" 方法
   的返回值。这个方法的返回值被用作与 *stop* 相关联的内部标志的新值；
   返回 false 将导致解释继续。

Cmd.preloop()

   钩方法当 "cmdloop()" 被调用时执行一次。方法是一个在 "Cmd" 中的存根
   ；它的存在是为了被子类覆盖。

Cmd.postloop()

   钩方法在 "cmdloop()" 即将返回时执行一次。这个方法是一个在 "Cmd" 中
   的存根；塔顶存在是为了被子类覆盖。

Instances of "Cmd" subclasses have some public instance variables:

Cmd.prompt

   发出提示以请求输入。

Cmd.identchars

   接受命令前缀的字符串。

Cmd.lastcmd

   看到最后一个非空命令前缀。

Cmd.cmdqueue

   排队的输入行列表。当需要新的输入时，在 "cmdloop()" 中检查 cmdqueue
   列表；如果它不是空的，它的元素将被按顺序处理，就像在提示符处输入一
   样。

Cmd.intro

   要作为简介或横幅发出的字符串。 可以通过给 "cmdloop()" 方法一个参数
   来覆盖它。

Cmd.doc_header

   如果帮助输出具有记录命令的段落，则发出头文件。

Cmd.misc_header

   如果帮助输出其他帮助主题的部分（即与 "do_*()" 方法没有关联的
   "help_*()" 方法），则发出头文件。

Cmd.undoc_header

   如果帮助输出未被记录命令的部分（即与 "help_*()" 方法没有关联的
   "do_*()" 方法），则发出头文件。

Cmd.ruler

   用于在帮助信息标题的下方绘制分隔符的字符，如果为空，则不绘制标尺线
   。 这个字符默认是 "'='" 。

Cmd.use_rawinput

   这是一个标志，默认为 true 。如果为 true ，, "cmdloop()" 使用
   "input()" 先是提示并且阅读下一个命令；如果为 false ，
   "sys.stdout.write()" 和 "sys.stdin.readline()" 被使用。（这意味着解
   释器将会自动支持类似于 **Emacs**的行编辑和命令历史记录按键操作，通
   过导入 "readline" 在支持它的系统上。）


Cmd 例子
========

The "cmd" module is mainly useful for building custom shells that let
a user work with a program interactively.

这部分提供了一个简单的例子来介绍如何使用一部分在 "turtle" 模块中的命令
构建一个 shell 。

基础的 turtle 命令比如 "forward()" 被添加进一个 "Cmd" 子类，方法名为
"do_forward()" 。参数被转换成数字并且分发至 turtle 模组中。 docstring
是 shell 提供的帮助实用程序。

例子也包含使用 "precmd()" 方法实现基础的记录和回放的功能，这个方法负责
将输入转换为小写并且将命令写入文件。 "do_playback()" 方法读取文件并添
加记录命令至 "cmdqueue" 用于即时回放:

   import cmd, sys
   from turtle import *

   class TurtleShell(cmd.Cmd):
       intro = 'Welcome to the turtle shell.   Type help or ? to list commands.\n'
       prompt = '(turtle) '
       file = None

       # ----- basic turtle commands -----
       def do_forward(self, arg):
           'Move the turtle forward by the specified distance:  FORWARD 10'
           forward(*parse(arg))
       def do_right(self, arg):
           'Turn turtle right by given number of degrees:  RIGHT 20'
           right(*parse(arg))
       def do_left(self, arg):
           'Turn turtle left by given number of degrees:  LEFT 90'
           left(*parse(arg))
       def do_goto(self, arg):
           'Move turtle to an absolute position with changing orientation.  GOTO 100 200'
           goto(*parse(arg))
       def do_home(self, arg):
           'Return turtle to the home position:  HOME'
           home()
       def do_circle(self, arg):
           'Draw circle with given radius an options extent and steps:  CIRCLE 50'
           circle(*parse(arg))
       def do_position(self, arg):
           'Print the current turtle position:  POSITION'
           print('Current position is %d %d\n' % position())
       def do_heading(self, arg):
           'Print the current turtle heading in degrees:  HEADING'
           print('Current heading is %d\n' % (heading(),))
       def do_color(self, arg):
           'Set the color:  COLOR BLUE'
           color(arg.lower())
       def do_undo(self, arg):
           'Undo (repeatedly) the last turtle action(s):  UNDO'
       def do_reset(self, arg):
           'Clear the screen and return turtle to center:  RESET'
           reset()
       def do_bye(self, arg):
           'Stop recording, close the turtle window, and exit:  BYE'
           print('Thank you for using Turtle')
           self.close()
           bye()
           return True

       # ----- record and playback -----
       def do_record(self, arg):
           'Save future commands to filename:  RECORD rose.cmd'
           self.file = open(arg, 'w')
       def do_playback(self, arg):
           'Playback commands from a file:  PLAYBACK rose.cmd'
           self.close()
           with open(arg) as f:
               self.cmdqueue.extend(f.read().splitlines())
       def precmd(self, line):
           line = line.lower()
           if self.file and 'playback' not in line:
               print(line, file=self.file)
           return line
       def close(self):
           if self.file:
               self.file.close()
               self.file = None

   def parse(arg):
       'Convert a series of zero or more numbers to an argument tuple'
       return tuple(map(int, arg.split()))

   if __name__ == '__main__':
       TurtleShell().cmdloop()

这是一个示例会话，其中 turtle shell 显示帮助功能，使用空行重复命令，以
及简单的记录和回放功能：

   Welcome to the turtle shell.   Type help or ? to list commands.

   (turtle) ?

   Documented commands (type help <topic>):
   ========================================
   bye     color    goto     home  playback  record  right
   circle  forward  heading  left  position  reset   undo

   (turtle) help forward
   Move the turtle forward by the specified distance:  FORWARD 10
   (turtle) record spiral.cmd
   (turtle) position
   Current position is 0 0

   (turtle) heading
   Current heading is 0

   (turtle) reset
   (turtle) circle 20
   (turtle) right 30
   (turtle) circle 40
   (turtle) right 30
   (turtle) circle 60
   (turtle) right 30
   (turtle) circle 80
   (turtle) right 30
   (turtle) circle 100
   (turtle) right 30
   (turtle) circle 120
   (turtle) right 30
   (turtle) circle 120
   (turtle) heading
   Current heading is 180

   (turtle) forward 100
   (turtle)
   (turtle) right 90
   (turtle) forward 100
   (turtle)
   (turtle) right 90
   (turtle) forward 400
   (turtle) right 90
   (turtle) forward 500
   (turtle) right 90
   (turtle) forward 400
   (turtle) right 90
   (turtle) forward 300
   (turtle) playback spiral.cmd
   Current position is 0 0

   Current heading is 0

   Current heading is 180

   (turtle) bye
   Thank you for using Turtle
