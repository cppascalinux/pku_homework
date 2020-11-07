"mailcap" --- Mailcap 文件处理
******************************

**源代码:** Lib/mailcap.py

======================================================================

Mailcap 文件可用来配置支持 MIME 的应用例如邮件阅读器和 Web 浏览器如何
响应具有不同 MIME 类型的文件。 （"mailcap" 这个名称源自短语"mail
capability"。） 例如，一个 mailcap 文件可能包含 "video/mpeg; xmpeg %s"
这样的行。 然后，如果用户遇到 MIME 类型为 *video/mpeg* 的邮件消息或
Web 文档时，"%s" 将被替换为一个文件名（通常是一个临时文件）并且将自动
启动 **xmpeg** 程序来查看该文件。

mailcap 格式的文档见 **RFC 1524**, "A User Agent Configuration
Mechanism For Multimedia Mail Format Information"，但它并不是一个因特
网标准。 不过，mailcap 文件在大多数 Unix 系统上都受到支持。

mailcap.findmatch(caps, MIMEtype, key='view', filename='/dev/null', plist=[])

   返回一个 2 元组；其中第一个元素是包含所要执行命令的字符串 (它可被传
   递给 "os.system()")，第二个元素是对应于给定 MIME 类型的 mailcap 条
   目。 如果找不到匹配的 MIME 类型，则将返回 "(None, None)"。

   *key* 是所需字段的名称，它代表要执行的活动类型；默认值是 'view'，因
   为在最通常的情况下你只是想要查看 MIME 类型数据的正文。 其他可能的值
   还有 'compose' 和 'edit'，分别用于想要创建给定 MIME 类型正文或修改
   现有正文数据的情况。 请参阅 **RFC 1524** 获取这些字段的完整列表。

   *filename* 是在命令行中用来替换 "%s" 的文件名；默认值 "'/dev/null'"
   几乎肯定不是你想要的，因此通常你要通过指定一个文件名来重载它。

   *plist* 可以是一个包含命名形参的列表；默认值只是一个空列表。 列表中
   的每个条目必须为包含形参名称的字符串、等于号 ("'='") 以及形参的值。
   Mailcap 条目可以包含形如 "%{foo}" 的命名形参，它将由名为 'foo' 的形
   参的值所替换。 例如，如果命令行 "showpartial %{id} %{number}
   %{total}" 是在一个 mailcap 文件中，并且 *plist* 被设为 "['id=1',
   'number=2', 'total=3']"，则结果命令行将为 "'showpartial 1 2 3'"。

   在 mailcap 文件中，可以指定可选的 "test" 字段来检测某些外部条件（例
   如所使用的机器架构或窗口系统）来确定是否要应用 mailcap 行。
   "findmatch()" 将自动检查此类条件并在检查未通过时跳过条目。

mailcap.getcaps()

   返回一个将 MIME 类型映射到 mailcap 文件条目列表的字典。 此字典必须
   被传给 "findmatch()" 函数。 条目会被存储为字典列表，但并不需要了解
   此表示形式的细节。

   此信息来自在系统中找到的所有 mailcap 文件。 用户的 mailcap 文件
   "$HOME/.mailcap" 中的设置将覆盖系统 mailcap 文件 "/etc/mailcap",
   "/usr/etc/mailcap" 和 "/usr/local/etc/mailcap" 中的设置。

一个用法示例:

   >>> import mailcap
   >>> d = mailcap.getcaps()
   >>> mailcap.findmatch(d, 'video/mpeg', filename='tmp1223')
   ('xmpeg tmp1223', {'view': 'xmpeg %s'})
