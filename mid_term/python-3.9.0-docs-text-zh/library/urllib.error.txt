"urllib.error" --- urllib.request 引发的异常类
**********************************************

**源代码：** Lib/urllib/error.py

======================================================================

"urllib.error" 模块为 "urllib.request" 所引发的异常定义了异常类。 基础
异常类是 "URLError"。

下列异常会被 "urllib.error" 按需引发：

exception urllib.error.URLError

   处理程序在遇到问题时会引发此异常（或其派生的异常）。 它是 "OSError"
   的一个子类。

   reason

      此错误的原因。 它可以是一个消息字符串或另一个异常实例。

   在 3.3 版更改: "URLError" 已被设为 "OSError" 而不是 "IOError" 的子
   类。

exception urllib.error.HTTPError

   虽然是一个异常（"URLError" 的一个子类），"HTTPError" 也可以作为一个
   非异常的文件类返回值（与 "urlopen()" 返所回的对象相同）。 这适用于
   处理特殊 HTTP 错误例如作为认证请求的时候。

   code

      一个 HTTP 状态码，具体定义见 **RFC 2616**。 这个数字的值对应于存
      放在 "http.server.BaseHTTPRequestHandler.responses" 代码字典中的
      某个值。

   reason

      这通常是一个解释本次错误原因的字符串。

   headers

      导致 "HTTPError" 的特定 HTTP 请求的 HTTP 响应头。

      3.4 新版功能.

exception urllib.error.ContentTooShortError(msg, content)

   此异常会在 "urlretrieve()" 函数检测到已下载的数据量小于期待的数据量
   （由 *Content-Length* 头给定）时被引发。 "content" 属性中将存放已下
   载（可能被截断）的数据。
