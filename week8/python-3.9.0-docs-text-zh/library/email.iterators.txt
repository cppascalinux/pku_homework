"email.iterators": 迭代器
*************************

**源代码:** Lib/email/iterators.py

======================================================================

通过 "Message.walk" 方法来迭代消息对象树是相当容易的。
"email.iterators" 模块提供了一些适用于消息对象树的高层级迭代器。

email.iterators.body_line_iterator(msg, decode=False)

   此函数会迭代 *msg* 的所有子部分中的所有载荷，逐行返回字符串载荷。
   它会跳过所有子部分的标头，并且它也会跳过任何包含不为 Python 字符串
   的载荷的子部分。 这基本上等价于使用 "readline()" 从一个文件读取消息
   的纯文本表示形式，并跳过所有中间的标头。

   可选的 *decode* 会被传递给 "Message.get_payload"。

email.iterators.typed_subpart_iterator(msg, maintype='text', subtype=None)

   此函数会迭代 *msg* 的所有子部分，只返回其中与 *maintype* 和
   *subtype* 所指定的 MIME 类型相匹配的子部分。

   请注意 *subtype* 是可选项；如果省略，则仅使用主类型来进行子部分
   MIME 类型的匹配。 *maintype* 也是可选项；它的默认值为 *text*。

   因此，在默认情况下 "typed_subpart_iterator()" 会返回每一个 MIME 类
   型为 *text/** 的子部分。

增加了以下函数作为有用的调试工具。 它 *不应当* 被视为该包所支持的公共
接口的组成部分。

email.iterators._structure(msg, fp=None, level=0, include_default=False)

   打印消息对象结构的内容类型的缩进表示形式。 例如:

      >>> msg = email.message_from_file(somefile)
      >>> _structure(msg)
      multipart/mixed
          text/plain
          text/plain
          multipart/digest
              message/rfc822
                  text/plain
              message/rfc822
                  text/plain
              message/rfc822
                  text/plain
              message/rfc822
                  text/plain
              message/rfc822
                  text/plain
          text/plain

   可选项 *fp* 是一个作为打印输出目标的文件类对象。 它必须适用于
   Python 的 "print()" 函数。 *level* 是供内部使用的。
   *include_default* 如果为真值，则会同时打印默认类型。
