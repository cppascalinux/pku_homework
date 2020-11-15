3. Python 的非正式介绍
**********************

在下面的例子中，通过提示符 (*>>>* 与 *...*) 的出现与否来区分输入和输出
：如果你想复现这些例子，当提示符出现后，你必须在提示符后键入例子中的每
一个词；不以提示符开头的那些行是解释器的输出。注意例子中某行中出现第二
个提示符意味着你必须键入一个空白行；这是用来结束多行命令的。

这个手册中的许多例子都包含注释，甚至交互性命令中也有。Python中的注释以
井号 "#" 开头，并且一直延伸到该文本行结束为止。注释可以出现在一行的开
头或者是空白和代码的后边，但是不能出现在字符串中间。字符串中的井号就是
井号。因为注释是用来阐明代码的，不会被 Python 解释，所以在键入这些例子
时，注释是可以被忽略的。

几个例子:

   # this is the first comment
   spam = 1  # and this is the second comment
             # ... and now a third!
   text = "# This is not a comment because it's inside quotes."


3.1. Python 作为计算器使用
==========================

让我们尝试一些简单的 Python 命令。启动解释器，等待界面中的提示符，
">>>" （这应该花不了多少时间）。


3.1.1. 数字
-----------

解释器就像一个简单的计算器一样：你可以在里面输入一个表达式然后它会写出
答案。 表达式的语法很直接：运算符 "+"、"-"、"*"、"/" 的用法和其他大部
分语言一样（比如 Pascal 或者 C 语言）；括号 ("()") 用来分组。比如:

   >>> 2 + 2
   4
   >>> 50 - 5*6
   20
   >>> (50 - 5*6) / 4
   5.0
   >>> 8 / 5  # division always returns a floating point number
   1.6

整数（比如 "2"、"4"、"20" ）的类型是 "int"，有小数部分的（比如 "5.0"、
"1.6" ）的类型是 "float"。 在这个手册的后半部分我们会看到更多的数字类
型。

除法运算 ("/") 永远返回浮点数类型。如果要做 *floor division* 得到一个
整数结果（忽略小数部分）你可以使用 "//" 运算符；如果要计算余数，可以使
用 "%"

   >>> 17 / 3  # classic division returns a float
   5.666666666666667
   >>>
   >>> 17 // 3  # floor division discards the fractional part
   5
   >>> 17 % 3  # the % operator returns the remainder of the division
   2
   >>> 5 * 3 + 2  # result * divisor + remainder
   17

在Python中，可以使用 "**" 运算符来计算乘方 [1]

   >>> 5 ** 2  # 5 squared
   25
   >>> 2 ** 7  # 2 to the power of 7
   128

等号 ("=") 用于给一个变量赋值。然后在下一个交互提示符之前不会有结果显
示出来:

   >>> width = 20
   >>> height = 5 * 9
   >>> width * height
   900

如果一个变量未定义(未赋值)，试图使用它时会向你提示错误:

   >>> n  # try to access an undefined variable
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
   NameError: name 'n' is not defined

Python中提供浮点数的完整支持；包含多种混合类型运算数的运算会把整数转换
为浮点数:

   >>> 4 * 3.75 - 1
   14.0

在交互模式下，上一次打印出来的表达式被赋值给变量 "_"。这意味着当你把
Python用作桌面计算器时，继续计算会相对简单，比如:

   >>> tax = 12.5 / 100
   >>> price = 100.50
   >>> price * tax
   12.5625
   >>> price + _
   113.0625
   >>> round(_, 2)
   113.06

这个变量应该被使用者当作是只读类型。不要向它显式地赋值——你会创建一个和
它名字相同独立的本地变量，它会使用魔法行为屏蔽内部变量。

除了 "int" 和 "float"，Python也支持其他类型的数字，例如 "Decimal" 或者
"Fraction"。Python 也内置对 复数 的支持，使用后缀 "j" 或者 "J" 就可以
表示虚数部分（例如 "3+5j" ）。


3.1.2. 字符串
-------------

除了数字，Python 也可以操作字符串。字符串有多种形式，可以使用单引号（
"'……'"），双引号（""……""）都可以获得同样的结果 [2]。反斜杠 "\" 可以用
来转义:

   >>> 'spam eggs'  # single quotes
   'spam eggs'
   >>> 'doesn\'t'  # use \' to escape the single quote...
   "doesn't"
   >>> "doesn't"  # ...or use double quotes instead
   "doesn't"
   >>> '"Yes," they said.'
   '"Yes," they said.'
   >>> "\"Yes,\" they said."
   '"Yes," they said.'
   >>> '"Isn\'t," they said.'
   '"Isn\'t," they said.'

在交互式解释器中，输出的字符串外面会加上引号，特殊字符会使用反斜杠来转
义。 虽然有时这看起来会与输入不一样（外面所加的引号可能会改变），但两
个字符串是相同的。 如果字符串中有单引号而没有双引号，该字符串外将加双
引号来表示，否则就加单引号。 "print()" 函数会生成可读性更强的输出，即
略去两边的引号，并且打印出经过转义的特殊字符:

   >>> '"Isn\'t," they said.'
   '"Isn\'t," they said.'
   >>> print('"Isn\'t," they said.')
   "Isn't," they said.
   >>> s = 'First line.\nSecond line.'  # \n means newline
   >>> s  # without print(), \n is included in the output
   'First line.\nSecond line.'
   >>> print(s)  # with print(), \n produces a new line
   First line.
   Second line.

如果你不希望前置了 "\" 的字符转义成特殊字符，可以使用 *原始字符串* 方
式，在引号前添加 "r" 即可:

   >>> print('C:\some\name')  # here \n means newline!
   C:\some
   ame
   >>> print(r'C:\some\name')  # note the r before the quote
   C:\some\name

字符串字面值可以跨行连续输入。一种方式是用三重引号：""""..."""" 或
"'''...'''"。字符串中的回车换行会自动包含到字符串中，如果不想包含，在
行尾添加一个 "\" 即可。如下例:

   print("""\
   Usage: thingy [OPTIONS]
        -h                        Display this usage message
        -H hostname               Hostname to connect to
   """)

将产生如下输出（注意最开始的换行没有包括进来）:

   Usage: thingy [OPTIONS]
        -h                        Display this usage message
        -H hostname               Hostname to connect to

字符串可以用 "+" 进行连接（粘到一起），也可以用 "*" 进行重复:

   >>> # 3 times 'un', followed by 'ium'
   >>> 3 * 'un' + 'ium'
   'unununium'

相邻的两个或多个 *字符串字面值* （引号引起来的字符）将会自动连接到一起
.

   >>> 'Py' 'thon'
   'Python'

把很长的字符串拆开分别输入的时候尤其有用:

   >>> text = ('Put several strings within parentheses '
   ...         'to have them joined together.')
   >>> text
   'Put several strings within parentheses to have them joined together.'

只能对两个字面值这样操作，变量或表达式不行:

   >>> prefix = 'Py'
   >>> prefix 'thon'  # can't concatenate a variable and a string literal
     File "<stdin>", line 1
       prefix 'thon'
                   ^
   SyntaxError: invalid syntax
   >>> ('un' * 3) 'ium'
     File "<stdin>", line 1
       ('un' * 3) 'ium'
                      ^
   SyntaxError: invalid syntax

如果你想连接变量，或者连接变量和字面值，可以用 "+" 号:

   >>> prefix + 'thon'
   'Python'

字符串是可以被 *索引* （下标访问）的，第一个字符索引是 0。单个字符并没
有特殊的类型，只是一个长度为一的字符串:

   >>> word = 'Python'
   >>> word[0]  # character in position 0
   'P'
   >>> word[5]  # character in position 5
   'n'

索引也可以用负数，这种会从右边开始数:

   >>> word[-1]  # last character
   'n'
   >>> word[-2]  # second-last character
   'o'
   >>> word[-6]
   'P'

注意 -0 和 0 是一样的，所以负数索引从 -1 开始。

除了索引，字符串还支持 *切片*。索引可以得到单个字符，而 *切片* 可以获
取子字符串:

   >>> word[0:2]  # characters from position 0 (included) to 2 (excluded)
   'Py'
   >>> word[2:5]  # characters from position 2 (included) to 5 (excluded)
   'tho'

注意切片的开始总是被包括在结果中，而结束不被包括。这使得 "s[:i] +
s[i:]" 总是等于 "s"

   >>> word[:2] + word[2:]
   'Python'
   >>> word[:4] + word[4:]
   'Python'

切片的索引有默认值；省略开始索引时默认为0，省略结束索引时默认为到字符
串的结束:

   >>> word[:2]   # character from the beginning to position 2 (excluded)
   'Py'
   >>> word[4:]   # characters from position 4 (included) to the end
   'on'
   >>> word[-2:]  # characters from the second-last (included) to the end
   'on'

您也可以这么理解切片：将索引视作指向字符 *之间* ，第一个字符的左侧标为
0，最后一个字符的右侧标为 *n* ，其中 *n* 是字符串长度。例如:

    +---+---+---+---+---+---+
    | P | y | t | h | o | n |
    +---+---+---+---+---+---+
    0   1   2   3   4   5   6
   -6  -5  -4  -3  -2  -1

第一行数标注了字符串非负的索引的位置，第二行标注了对应的负的索引。那么
从 *i* 到 *j* 的切片就包括了标有 *i* 和 *j* 的位置之间的所有字符。

对于使用非负索引的切片，如果索引不越界，那么得到的切片长度就是起止索引
之差。例如， "word[1:3]" 的长度为2.

使用过大的索引会产生一个错误:

   >>> word[42]  # the word only has 6 characters
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
   IndexError: string index out of range

但是，切片中的越界索引会被自动处理:

   >>> word[4:42]
   'on'
   >>> word[42:]
   ''

Python 中的字符串不能被修改，它们是  *immutable* 的。因此，向字符串的
某个索引位置赋值会产生一个错误:

   >>> word[0] = 'J'
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
   TypeError: 'str' object does not support item assignment
   >>> word[2:] = 'py'
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
   TypeError: 'str' object does not support item assignment

如果需要一个不同的字符串，应当新建一个:

   >>> 'J' + word[1:]
   'Jython'
   >>> word[:2] + 'py'
   'Pypy'

内建函数 "len()" 返回一个字符串的长度:

   >>> s = 'supercalifragilisticexpialidocious'
   >>> len(s)
   34

参见:

  文本序列类型 --- str
     字符串是一种 *序列类型* ，因此也支持序列类型的各种操作。

  字符串的方法
     字符串支持许多变换和查找的方法。

  格式化字符串字面值
     内嵌表达式的字符串字面值。

  格式字符串语法
     使用 "str.format()" 进行字符串格式化。

  printf 风格的字符串格式化
     这里详述了使用 "%" 运算符进行字符串格式化。


3.1.3. 列表
-----------

Python 中可以通过组合一些值得到多种 *复合* 数据类型。其中最常用的 *列
表* ，可以通过方括号括起、逗号分隔的一组值得到。一个 *列表* 可以包含不
同类型的元素，但通常使用时各个元素类型相同:

   >>> squares = [1, 4, 9, 16, 25]
   >>> squares
   [1, 4, 9, 16, 25]

和字符串（以及各种内置的 *sequence* 类型）一样，列表也支持索引和切片:

   >>> squares[0]  # indexing returns the item
   1
   >>> squares[-1]
   25
   >>> squares[-3:]  # slicing returns a new list
   [9, 16, 25]

所有的切片操作都返回一个包含所请求元素的新列表。 这意味着以下切片操作
会返回列表的一个 浅拷贝:

   >>> squares[:]
   [1, 4, 9, 16, 25]

列表同样支持拼接操作:

   >>> squares + [36, 49, 64, 81, 100]
   [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]

与 *immutable* 的字符串不同, 列表是一个 *mutable* 类型，就是说，它自己
的内容可以改变:

   >>> cubes = [1, 8, 27, 65, 125]  # something's wrong here
   >>> 4 ** 3  # the cube of 4 is 64, not 65!
   64
   >>> cubes[3] = 64  # replace the wrong value
   >>> cubes
   [1, 8, 27, 64, 125]

你也可以在列表结尾，通过 "append()" *方法* 添加新元素 (我们会在后面解
释更多关于方法的内容):

   >>> cubes.append(216)  # add the cube of 6
   >>> cubes.append(7 ** 3)  # and the cube of 7
   >>> cubes
   [1, 8, 27, 64, 125, 216, 343]

给切片赋值也是可以的，这样甚至可以改变列表大小，或者把列表整个清空:

   >>> letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
   >>> letters
   ['a', 'b', 'c', 'd', 'e', 'f', 'g']
   >>> # replace some values
   >>> letters[2:5] = ['C', 'D', 'E']
   >>> letters
   ['a', 'b', 'C', 'D', 'E', 'f', 'g']
   >>> # now remove them
   >>> letters[2:5] = []
   >>> letters
   ['a', 'b', 'f', 'g']
   >>> # clear the list by replacing all the elements with an empty list
   >>> letters[:] = []
   >>> letters
   []

内置函数 "len()" 也可以作用到列表上:

   >>> letters = ['a', 'b', 'c', 'd']
   >>> len(letters)
   4

也可以嵌套列表 (创建包含其他列表的列表), 比如说:

   >>> a = ['a', 'b', 'c']
   >>> n = [1, 2, 3]
   >>> x = [a, n]
   >>> x
   [['a', 'b', 'c'], [1, 2, 3]]
   >>> x[0]
   ['a', 'b', 'c']
   >>> x[0][1]
   'b'


3.2. 走向编程的第一步
=====================

当然，我们可以将 Python 用于更复杂的任务，而不是仅仅两个和两个一起添加
。 例如，我们可以编写 斐波那契数列 的初始子序列，如下所示:

   >>> # Fibonacci series:
   ... # the sum of two elements defines the next
   ... a, b = 0, 1
   >>> while a < 10:
   ...     print(a)
   ...     a, b = b, a+b
   ...
   0
   1
   1
   2
   3
   5
   8

这个例子引入了几个新的特点。

* 第一行含有一个 *多重赋值*: 变量 "a" 和 "b" 同时得到了新值 0 和 1.
  最后一行又用了一次多重赋值, 这体现出了右手边的表达式，在任何赋值发生
  之前就被求值了。右手边的表达式是从左到右被求值的。

* "while" 循环只要它的条件（这里指： "a < 10"）保持为真就会一直执行。
  Python 和 C 一样，任何非零整数都为真；零为假。这个条件也可以是字符串
  或是列表的值，事实上任何序列都可以；长度非零就为真，空序列就为假。在
  这个例子里，判断条件是一个简单的比较。标准的比较操作符的写法和 C 语
  言里是一样： "<" （小于）、 ">" （大于）、 "==" （等于）、 "<=" （小
  于或等于)、 ">=" （大于或等于）以及 "!=" （不等于）。

* *循环体* 是 *缩进的* ：缩进是 Python 组织语句的方式。在交互式命令行
  里，你得给每个缩进的行敲下 Tab 键或者（多个）空格键。实际上用文本编
  辑器的话，你要准备更复杂的输入方式；所有像样的文本编辑器都有自动缩进
  的设置。交互式命令行里，当一个组合的语句输入时, 需要在最后敲一个空白
  行表示完成（因为语法分析器猜不出来你什么时候打的是最后一行）。注意，
  在同一块语句中的每一行，都要缩进相同的长度。

* "print()" 函数将所有传进来的参数值打印出来. 它和直接输入你要显示的表
  达式(比如我们之前在计算器的例子里做的)不一样， print() 能处理多个参
  数，包括浮点数，字符串。 字符串会打印不带引号的内容, 并且在参数项之
  间会插入一个空格, 这样你就可以很好的把东西格式化, 像这样:

     >>> i = 256*256
     >>> print('The value of i is', i)
     The value of i is 65536

  关键字参数 *end* 可以用来取消输出后面的换行, 或是用另外一个字符串来
  结尾:

     >>> a, b = 0, 1
     >>> while a < 1000:
     ...     print(a, end=',')
     ...     a, b = b, a+b
     ...
     0,1,1,2,3,5,8,13,21,34,55,89,144,233,377,610,987,

-[ 脚注 ]-

[1] 因为 "**" 比 "-" 有更高的优先级, 所以 "-3**2" 会被解释成 "-(3**2)"
    ，因此结果是 "-9".  为了避免这个并且得到结果 "9", 你可以用这个式子
    "(-3)**2".

[2] 和其他语言不一样的是, 特殊字符比如说 "\n" 在单引号 ("'...'") 和双
    引号 (""..."") 里有一样的意义. 这两种引号唯一的区别是，你不需要在
    单引号里转义双引号 """ (但是你必须把单引号转义成 "\'") ， 反之亦然
    .
