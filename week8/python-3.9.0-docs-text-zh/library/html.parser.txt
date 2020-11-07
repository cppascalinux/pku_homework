"html.parser" --- 简单的 HTML 和 XHTML 解析器
*********************************************

**源代码：** Lib/html/parser.py

======================================================================

这个模块定义了一个 "HTMLParser" 类，为 HTML（超文本标记语言）和 XHTML
文本文件解析提供基础。

class html.parser.HTMLParser(*, convert_charrefs=True)

   创建一个能解析无效标记的解析器实例。

   如果 *convert_charrefs* 为 "True" (默认值)，则所有字符引用(
   "script"/"style"   元素中的除外)都会自动转换为相应的 Unicode 字符。

   一个 "HTMLParser" 类的实例用来接受 HTML 数据，并在标记开始、标记结
   束、文本、注释和其他元素标记出现的时候调用对应的方法。要实现具体的
   行为，请使用 "HTMLParser" 的子类并重载其方法。

   这个解析器不检查结束标记是否与开始标记匹配，也不会因外层元素完毕而
   隐式关闭了的元素引发结束标记处理。

   在 3.4 版更改: *convert_charrefs* 关键字参数被添加。

   在 3.5 版更改: *convert_charrefs* 参数的默认值现在为 "True"。


HTML 解析器的示例程序
=====================

下面是简单的 HTML 解析器的一个基本示例，使用 "HTMLParser" 类，当遇到开
始标记、结束标记以及数据的时候将内容打印出来。

   from html.parser import HTMLParser

   class MyHTMLParser(HTMLParser):
       def handle_starttag(self, tag, attrs):
           print("Encountered a start tag:", tag)

       def handle_endtag(self, tag):
           print("Encountered an end tag :", tag)

       def handle_data(self, data):
           print("Encountered some data  :", data)

   parser = MyHTMLParser()
   parser.feed('<html><head><title>Test</title></head>'
               '<body><h1>Parse me!</h1></body></html>')

输出是:

   Encountered a start tag: html
   Encountered a start tag: head
   Encountered a start tag: title
   Encountered some data  : Test
   Encountered an end tag : title
   Encountered an end tag : head
   Encountered a start tag: body
   Encountered a start tag: h1
   Encountered some data  : Parse me!
   Encountered an end tag : h1
   Encountered an end tag : body
   Encountered an end tag : html


"HTMLParser" 方法
=================

"HTMLParser" 实例有下列方法：

HTMLParser.feed(data)

   填充一些文本到解析器中。如果包含完整的元素，则被处理；如果数据不完
   整，将被缓冲直到更多的数据被填充，或者 "close()" 被调用。*data* 必
   须为 "str" 类型。

HTMLParser.close()

   如同后面跟着一个文件结束标记一样，强制处理所有缓冲数据。这个方法能
   被派生类重新定义，用于在输入的末尾定义附加处理，但是重定义的版本应
   当始终调用基类 "HTMLParser" 的 "close()" 方法。

HTMLParser.reset()

   重置实例。丢失所有未处理的数据。在实例化阶段被隐式调用。

HTMLParser.getpos()

   返回当前行号和偏移值。

HTMLParser.get_starttag_text()

   返回最近打开的开始标记中的文本。 结构化处理时通常应该不需要这个，但
   在处理“已部署”的 HTML 或是在以最小改变来重新生成输入时可能会有用处
   （例如可以保留属性间的空格等）。

下列方法将在遇到数据或者标记元素的时候被调用。他们需要在子类中重载。基
类的实现中没有任何实际操作（除了 "handle_startendtag()" ）：

HTMLParser.handle_starttag(tag, attrs)

   这个方法在标签开始的时候被调用（例如： "<div id="main">" ）。

   *tag* 参数是小写的标记名。*attrs* 参数是一个 "(name, value)" 形式的
   列表，包含了所有在标记的 "<>"  括号中找到的属性。*name* 转换为小写
   ，*value* 的引号被去除，字符和实体引用都会被替换。

   实例中，对于标签 "<A HREF="https://www.cwi.nl/">"，这个方法将以下列
   形式被调用 "handle_starttag('a', [('href',
   'https://www.cwi.nl/')])" 。

   "html.entities" 中的所有实体引用，会被替换为属性值。

HTMLParser.handle_endtag(tag)

   此方法被用来处理元素的结束标记（例如： "</div>" ）。

   *tag* 参数是小写的标签名。

HTMLParser.handle_startendtag(tag, attrs)

   类似于 "handle_starttag()", 只是在解析器遇到 XHTML 样式的空标记时被
   调用（ "<img ... />"）。这个方法能被需要这种特殊词法信息的子类重载
   ；默认实现仅简单调用 "handle_starttag()" 和 "handle_endtag()" 。

HTMLParser.handle_data(data)

   这个方法被用来处理任意数据（例如：文本节点和 "<script>...</script>"
   以及 "<style>...</style>" 中的内容）。

HTMLParser.handle_entityref(name)

   这个方法被用于处理 "&name;" 形式的命名字符引用（例如 "&gt;"），其中
   *name* 是通用的实体引用（例如： "'gt'"）。如果 *convert_charrefs*
   为 "True"，该方法永远不会被调用。

HTMLParser.handle_charref(name)

   这个方法被用来处理 "&#NNN;" 和 "&#xNNN;" 形式的十进制和十六进制字符
   引用。例如，"&gt;" 等效的十进制形式为 "&#62;" ，而十六进制形式为
   "&#x3E;" ；在这种情况下，方法将收到  "'62'" 或 "'x3E'" 。如果
   *convert_charrefs* 为 "True" ，则该方法永远不会被调用。

HTMLParser.handle_comment(data)

   这个方法在遇到注释的时候被调用（例如： "<!--comment-->" ）。

   例如， "<!-- comment -->" 这个注释会用 "' comment '" 作为参数调用此
   方法。

   Internet Explorer 条件注释（condcoms）的内容也被发送到这个方法，因
   此，对于 "<!--[if IE 9]>IE9-specific content<![endif]-->" ，这个方
   法将接收到 "'[if IE 9]>IE9-specific content<![endif]'" 。

HTMLParser.handle_decl(decl)

   这个方法用来处理 HTML doctype 申明（例如 "<!DOCTYPE html>" ）。

   *decl* 形参为 "<!...>" 标记中的所有内容（例如： "'DOCTYPE html'" ）
   。

HTMLParser.handle_pi(data)

   此方法在遇到处理指令的时候被调用。*data* 形参将包含整个处理指令。例
   如，对于处理指令 "<?proc color='red'>" ，这个方法将以
   "handle_pi("proc color='red'")" 形式被调用。它旨在被派生类重载；基
   类实现中无任何实际操作。

   注解:

     "HTMLParser" 类使用 SGML 语法规则处理指令。使用 "'?'" 结尾的
     XHTML 处理指令将导致 "'?'" 包含在 *data* 中。

HTMLParser.unknown_decl(data)

   当解析器读到无法识别的声明时，此方法被调用。

   *data* 形参为 "<![...]>" 标记中的所有内容。某些时候对派生类的重载很
   有用。基类实现中无任何实际操作。


示例
====

下面的类实现了一个解析器，用于更多示例的演示:

   from html.parser import HTMLParser
   from html.entities import name2codepoint

   class MyHTMLParser(HTMLParser):
       def handle_starttag(self, tag, attrs):
           print("Start tag:", tag)
           for attr in attrs:
               print("     attr:", attr)

       def handle_endtag(self, tag):
           print("End tag  :", tag)

       def handle_data(self, data):
           print("Data     :", data)

       def handle_comment(self, data):
           print("Comment  :", data)

       def handle_entityref(self, name):
           c = chr(name2codepoint[name])
           print("Named ent:", c)

       def handle_charref(self, name):
           if name.startswith('x'):
               c = chr(int(name[1:], 16))
           else:
               c = chr(int(name))
           print("Num ent  :", c)

       def handle_decl(self, data):
           print("Decl     :", data)

   parser = MyHTMLParser()

解析一个文档类型声明:

   >>> parser.feed('<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" '
   ...             '"http://www.w3.org/TR/html4/strict.dtd">')
   Decl     : DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd"

解析一个具有一些属性和标题的元素:

   >>> parser.feed('<img src="python-logo.png" alt="The Python logo">')
   Start tag: img
        attr: ('src', 'python-logo.png')
        attr: ('alt', 'The Python logo')
   >>>
   >>> parser.feed('<h1>Python</h1>')
   Start tag: h1
   Data     : Python
   End tag  : h1

"script" 和 "style" 元素中的内容原样返回，无需进一步解析:

   >>> parser.feed('<style type="text/css">#python { color: green }</style>')
   Start tag: style
        attr: ('type', 'text/css')
   Data     : #python { color: green }
   End tag  : style

   >>> parser.feed('<script type="text/javascript">'
   ...             'alert("<strong>hello!</strong>");</script>')
   Start tag: script
        attr: ('type', 'text/javascript')
   Data     : alert("<strong>hello!</strong>");
   End tag  : script

解析注释:

   >>> parser.feed('<!-- a comment -->'
   ...             '<!--[if IE 9]>IE-specific content<![endif]-->')
   Comment  :  a comment
   Comment  : [if IE 9]>IE-specific content<![endif]

解析命名或数字形式的字符引用，并把他们转换到正确的字符（注意：这 3 种
转义都是 "'>'" ）:

   >>> parser.feed('&gt;&#62;&#x3E;')
   Named ent: >
   Num ent  : >
   Num ent  : >

填充不完整的块给 "feed()" 执行，"handle_data()" 可能会多次调用（除非
*convert_charrefs* 被设置为 "True" ）:

   >>> for chunk in ['<sp', 'an>buff', 'ered ', 'text</s', 'pan>']:
   ...     parser.feed(chunk)
   ...
   Start tag: span
   Data     : buff
   Data     : ered
   Data     : text
   End tag  : span

解析无效的 HTML (例如：未引用的属性）也能正常运行:

   >>> parser.feed('<p><a class=link href=#main>tag soup</p ></a>')
   Start tag: p
   Start tag: a
        attr: ('class', 'link')
        attr: ('href', '#main')
   Data     : tag soup
   End tag  : p
   End tag  : a
