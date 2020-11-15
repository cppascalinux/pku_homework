字符串转换与格式化
******************

用于数字转换和格式化字符串输出的函数

int PyOS_snprintf(char *str, size_t size, const char *format, ...)

   根据格式字符串 *format* 和额外参数，输出不超过 *size* 字节到 *str*
   。请参见Unix手册页 *snprintf(2)* 。

int PyOS_vsnprintf(char *str, size_t size, const char *format, va_list va)

   根据格式字符串 *format* 和 变量参数列表 *va* ，不能输出超过 *size*
   字节到 *str* 。请参见Unix手册页 *vsnprintf(2)* 。

"PyOS_snprintf()" 和 "PyOS_vsnprintf()" 包装 C 标准库函数 "snprintf()"
和 "vsnprintf()" 。它们的目的是保证在极端情况下的一致行为，而标准 C 的
函数则不然。

包装器确保 *str*[*size*-1] 在返回时始终是 "'\0'" 。它们从不写入超过
*size* 字节（包括结尾的 "'\0'" ）到字符串。两函数都需要满足 "str !=
NULL" , "size > 0" 和 "format != NULL" 。

如果平台没有 "vsnprintf()" 而且缓冲区大小需要避免截断超出 *size* 512
字节以上，Python 会以一个 "Py_FatalError()" 来中止。

这些函数的返回值（ *rv* ）应按照以下规则被解释：

* 当 "0 <= rv < size" ，输出转换成功而且 *rv* 个字符被写入 *str* （不
  包含末尾 *str*[*rv*] 的 "'\0'" 字节）

* 当 "rv >= size" ，输出转换被截断并且成功需要一个带有 "rv + 1" 字节的
  缓冲区。在这种情况下， *str*[*size*-1] 的值是 "'\0'" 。

* 当 "rv < 0" ，会发生一些不好的事情。 在这种情况下， *str*[*size*-1]
  的值也是 "'\0'" ， 但是 *str* 的其余部分未被定义。错误的确切原因取决
  于底层平台。

以下函数提供与语言环境无关的字符串到数字转换。

double PyOS_string_to_double(const char *s, char **endptr, PyObject *overflow_exception)

   将字符串 "s" 转换为 "double" 类型，失败时引发Python异常。接受的字符
   串的集合对应于被 Python 的 "float()" 构造函数接受的字符串的集合，除
   了 "s" 必须没有前导或尾随空格。转换必须独立于当前的区域。

   如果 "endptr" 是 "NULL" ，转换整个字符串。引发 "ValueError" 并且 返
   回 "-1.0" 如果字符串不是浮点数的有效的表达方式。

   如果 "endptr" 不是 "NULL" ，尽可能多的转换字符串并将 "*endptr" 设置
   为指向第一个未转换的字符。如果字符串的初始段不是浮点数的有效的表达
   方式，将 "*endptr" 设置为指向字符串的开头，引发 ValueError 异常，并
   且返回 "-1.0" 。

   如果 "s" 表示一个太大而不能存储在一个浮点数中的值（比方说，
   ""1e500"" 在许多平台上是一个字符串）然后如果 "overflow_exception"
   是 "NULL" 返回 "Py_HUGE_VAL" （用适当的符号）并且不设置任何异常。
   在其他方面， "overflow_exception" 必须指向一个 Python 异常对象；引
   发异常并返回 "-1.0" 。在这两种情况下，设置 "*endptr" 指向转换值之后
   的第一个字符。

   如果在转换期间发生任何其他错误（比如一个内存不足的错误），设置适当
   的 Python 异常并且返回 "-1.0" 。

   3.1 新版功能.

char* PyOS_double_to_string(double val, char format_code, int precision, int flags, int *ptype)

   转换 "double" *val* 为一个使用 *format_code*， *precision* 和
   *flags* 的字符串

   *格式码* 必须是以下其中之一, "'e'", "'E'", "'f'", "'F'", "'g'",
   "'G'" 或者 "'r'"。对于 "'r'" , 提供的 *精度* 必须是0。"'r'" 格式码
   指定了标准函数 "repr()" 格式。

   *flags* 可以为零或者其他值 "Py_DTSF_SIGN", "Py_DTSF_ADD_DOT_0" 或
   "Py_DTSF_ALT" 或其组合：

   * "Py_DTSF_SIGN" 表示总是在返回的字符串前附加一个符号字符，即使
     *val* 为非负数。

   * "Py_DTSF_ADD_DOT_0" 表示确保返回的字符串看起来不像是一个整数。

   * "Py_DTSF_ALT" 表示应用 "替代的" 格式化规则。 相关细节请参阅
     "PyOS_snprintf()" "'#'" 定义文档。

   如果 *ptype* 不为 "NULL"，则它指向的值将被设为 "Py_DTST_FINITE",
   "Py_DTST_INFINITE" 或 "Py_DTST_NAN" 中的一个，分别表示 *val* 是一个
   有限数字、无限数字或非数字。

   返回值是一个指向包含转换后字符串的 *buffer* 的指针，如果转换失败则
   为 "NULL"。 调用方要负责调用 "PyMem_Free()" 来释放返回的字符串。

   3.1 新版功能.

int PyOS_stricmp(const char *s1, const char *s2)

   字符串不区分大小写。该函数几乎与 "strcmp()" 的工作方式相同，只是它
   忽略了大小写。

int PyOS_strnicmp(const char *s1, const char *s2, Py_ssize_t  size)

   字符串不区分大小写。该函数几乎与 "strncmp()" 的工作方式相同，只是它
   忽略了大小写。
