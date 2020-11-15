"uu" --- 对 uuencode 文件进行编码与解码
***************************************

**源代码:** Lib/uu.py

======================================================================

此模块使用 uuencode 格式来编码和解码文件，以便任意二进制数据可通过仅限
ASCII 码的连接进行传输。 在任何要求文件参数的地方，这些方法都接受文件
类对象。 为了保持向下兼容，也接受包含路径名称的字符串，并且将打开相应
的文件进行读写；路径名称 "'-'" 被解读为标准输入或输出。 但是，此接口已
被弃用；在 Windows 中调用者最好是自行打开文件，并在需要时确保模式为
"'rb'" or "'wb'"。

此代码由 Lance Ellinghouse 贡献，并由 Jack Jansen 修改。

"uu" 模块定义了以下函数：

uu.encode(in_file, out_file, name=None, mode=None, *, backtick=False)

   使用 uuencode 将 *in_file* 文件编码为 *out_file* 文件。 经过
   uuencoded 编码的文件将具有指定 *name* 和 *mode* 作为解码该文件默认
   结果的标头。 默认值会相应地从 *in_file* 或 "'-'" 以及 "0o666" 中提
   取。 如果 *backtick* 为真值，零会用 "'`'" 而不是空格来表示。

   在 3.7 版更改: 增加 *backtick* 参数

uu.decode(in_file, out_file=None, mode=None, quiet=False)

   调用此函数会解码 uuencod 编码的 *in_file* 文件并将结果放入
   *out_file* 文件。 如果 *out_file* 是一个路径名称，*mode* 会在必须创
   建文件时用于设置权限位。 *out_file* 和 *mode* 的默认值会从 uuencode
   标头中提取。 但是，如果标头中指定的文件已存在，则会引发 "uu.Error"
   。

   如果输入由不正确的 uuencode 编码器生成，"decode()" 可能会打印一条警
   告到标准错误 ，这样 Python 可以从该错误中恢复。 将 *quiet* 设为真值
   可以屏蔽此警告。

exception uu.Error

   "Exception" 的子类，此异常可由 "uu.decode()" 在多种情况下引发，如上
   文所述，此外还包括格式错误的标头或被截断的输入文件等。

参见:

  模块 "binascii"
     支持模块，包含ASCII到二进制和二进制到ASCII转换。
