"token" --- 与Python解析树一起使用的常量
****************************************

**源码：** Lib/token.py

======================================================================

此模块提供表示解析树（终端令牌）的叶节点的数值的常量。 请参阅 Python
发行版中的文件 "Grammar/Grammar" ，以获取语言语法上下文中名称的定义。
名称映射到的特定数值可能会在 Python 版本之间更改。

该模块还提供从数字代码到名称和一些函数的映射。 这些函数镜像了 Python C
头文件中的定义。

token.tok_name

   将此模块中定义的常量的数值映射回名称字符串的字典，允许生成更加人类
   可读的解析树表示。

token.ISTERMINAL(x)

   对终端标记值返回 "True"。

token.ISNONTERMINAL(x)

   对非终端标记值返回 "True"。

token.ISEOF(x)

   如果 *x* 是表示输入结束的标记则返回 "True"。

标记常量是：

token.ENDMARKER

token.NAME

token.NUMBER

token.STRING

token.NEWLINE

token.INDENT

token.DEDENT

token.LPAR

   Token value for ""("".

token.RPAR

   Token value for "")"".

token.LSQB

   Token value for ""["".

token.RSQB

   Token value for ""]"".

token.COLON

   Token value for "":"".

token.COMMA

   Token value for "","".

token.SEMI

   Token value for "";"".

token.PLUS

   Token value for ""+"".

token.MINUS

   Token value for ""-"".

token.STAR

   Token value for ""*"".

token.SLASH

   Token value for ""/"".

token.VBAR

   Token value for ""|"".

token.AMPER

   Token value for ""&"".

token.LESS

   Token value for ""<"".

token.GREATER

   Token value for "">"".

token.EQUAL

   Token value for ""="".

token.DOT

   Token value for ""."".

token.PERCENT

   Token value for ""%"".

token.LBRACE

   Token value for ""{"".

token.RBRACE

   Token value for ""}"".

token.EQEQUAL

   Token value for ""=="".

token.NOTEQUAL

   Token value for ""!="".

token.LESSEQUAL

   Token value for ""<="".

token.GREATEREQUAL

   Token value for "">="".

token.TILDE

   Token value for ""~"".

token.CIRCUMFLEX

   Token value for ""^"".

token.LEFTSHIFT

   Token value for ""<<"".

token.RIGHTSHIFT

   Token value for "">>"".

token.DOUBLESTAR

   Token value for ""**"".

token.PLUSEQUAL

   Token value for ""+="".

token.MINEQUAL

   Token value for ""-="".

token.STAREQUAL

   Token value for ""*="".

token.SLASHEQUAL

   Token value for ""/="".

token.PERCENTEQUAL

   Token value for ""%="".

token.AMPEREQUAL

   Token value for ""&="".

token.VBAREQUAL

   Token value for ""|="".

token.CIRCUMFLEXEQUAL

   Token value for ""^="".

token.LEFTSHIFTEQUAL

   Token value for ""<<="".

token.RIGHTSHIFTEQUAL

   Token value for "">>="".

token.DOUBLESTAREQUAL

   Token value for ""**="".

token.DOUBLESLASH

   Token value for ""//"".

token.DOUBLESLASHEQUAL

   Token value for ""//="".

token.AT

   Token value for ""@"".

token.ATEQUAL

   Token value for ""@="".

token.RARROW

   Token value for ""->"".

token.ELLIPSIS

   Token value for ""..."".

token.COLONEQUAL

   Token value for "":="".

token.OP

token.AWAIT

token.ASYNC

token.TYPE_IGNORE

token.TYPE_COMMENT

token.ERRORTOKEN

token.N_TOKENS

token.NT_OFFSET

C 标记生成器不使用以下标记类型值，但 "tokenize" 模块需要这些标记类型值
。

token.COMMENT

   标记值用于表示注释。

token.NL

   标记值用于表示非终止换行符。 "NEWLINE" 标记表示 Python 代码逻辑行的
   结束；当在多条物理线路上继续执行逻辑代码行时，会生成 "NL" 标记。

token.ENCODING

   指示用于将源字节解码为文本的编码的标记值。 "tokenize.tokenize()" 返
   回的第一个标记将始终是一个 "ENCODING" 标记。

token.TYPE_COMMENT

   Token value indicating that a type comment was recognized.  Such
   tokens are only produced when "ast.parse()" is invoked with
   "type_comments=True".

在 3.5 版更改: 补充 "AWAIT" 和 "ASYNC" 标记。

在 3.7 版更改: 补充 "COMMENT" 、 "NL" 和 "ENCODING" 标记。

在 3.7 版更改: 移除 "AWAIT" 和 "ASYNC" 标记。 "async" 和 "await" 现在
被标记为 "NAME" 标记。

在 3.8 版更改: Added "TYPE_COMMENT", "TYPE_IGNORE", "COLONEQUAL".
Added "AWAIT" and "ASYNC" tokens back (they're needed to support
parsing older Python versions for "ast.parse()" with "feature_version"
set to 6 or lower).
