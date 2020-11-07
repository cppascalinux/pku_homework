"email.errors": 异常和缺陷类
****************************

**源代码:** Lib/email/errors.py

======================================================================

以下异常类在 "email.errors" 模块中定义：

exception email.errors.MessageError

   这是 "email" 包可以引发的所有异常的基类。 它源自标准异常
   "Exception" 类，这个类没有定义其他方法。

exception email.errors.MessageParseError

   这是由 "Parser" 类引发的异常的基类。它派生自 "MessageError"。
   "headerregistry" 使用的解析器也在内部使用这个类。

exception email.errors.HeaderParseError

   在解析消息的 **RFC 5322** 标头时，某些错误条件下会触发，此类派生自
   "MessageParseError"。 如果在调用方法时内容类型未知，则
   "set_boundary()" 方法将引发此错误。 当尝试创建一个看起来包含嵌入式
   标头的标头时 "Header" 可能会针对某些 base64 解码错误引发此错误（也
   就是说，应该是一个 没有前导空格并且看起来像标题的延续行）。

exception email.errors.BoundaryError

   已弃用和不再使用的。

exception email.errors.MultipartConversionError

   当使用 "add_payload()" 将有效负载添加到 "Message" 对象时，有效负载
   已经是一个标量，而消息的 *Content-Type* 主类型不是 *multipart* 或者
   缺少时触发该异常。 "MultipartConversionError" 多重继承自
   "MessageError" 和内置的 "TypeError"。

   由于 "Message.add_payload()" 已被弃用，此异常实际上极少会被引发。
   但是如果在派生自 "MIMENonMultipart" 的类 (例如 "MIMEImage") 的实例
   上调用 "attach()" 方法也可以引发此异常。

以下是 "FeedParser" 在解析消息时可发现的缺陷列表。 请注意这些缺陷会在
问题被发现时加入到消息中，因此举例来说，如果某条嵌套在
*multipart/alternative* 中的消息具有错误的标头，该嵌套消息对象就会有一
条缺陷，但外层消息对象则没有。

所有缺陷类都是 "email.errors.MessageDefect" 的子类。

* "NoBoundaryInMultipartDefect" -- 一条消息宣称有多个部分，但却没有
  *boundary* 形参。

* "StartBoundaryNotFoundDefect" -- 在 *Content-Type* 标头中宣称的开始
  边界无法被找到。

* "CloseBoundaryNotFoundDefect" -- 找到了开始边界，但相应的结束边界无
  法被找到。

  3.3 新版功能.

* "FirstHeaderLineIsContinuationDefect" -- 消息以一个继续行作为其第一
  个标头行。

* "MisplacedEnvelopeHeaderDefect" - 在标头块中间发现了一个 "Unix From"
  标头。

* "MissingHeaderBodySeparatorDefect" - 在解析没有前缀空格但又不包含
  ':' 的标头期间找到一行内容。 解析将假定该行表示消息体的第一行以继续
  执行。

  3.3 新版功能.

* "MalformedHeaderDefect" -- 找到一个缺失了冒号或格式错误的标头。

  3.3 版后已移除: 此缺陷在近几个 Python 版本中已不再使用。

* "MultipartInvariantViolationDefect" -- 一条消息宣称为 *multipart*，
  但无法找到任何子部分。 请注意当一条消息有此缺陷时，其
  "is_multipart()" 方法可能返回 "False"，即使其内容类型宣称为
  *multipart*。

* "InvalidBase64PaddingDefect" -- 当解码一个 base64 编码的字节分块时，
  填充的数据不正确。 虽然添加了足够的填充数据以执行解码，但作为结果的
  已解码字节串可能无效。

* "InvalidBase64CharactersDefect" -- 当解码一个 base64 编码的字节分块
  时，遇到了 base64 字符表以外的字符。 这些字符会被忽略，但作为结果的
  已解码字节串可能无效。

* "InvalidBase64LengthDefect" -- 当解码一个 base64 编码的字节分块时，
  非填充 base64 字符的数量无效（比 4 的倍数多 1）。 已编码分块会保持原
  样。
