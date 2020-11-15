旧缓冲协议
**********

3.0 版后已移除.

这些函数是 Python 2 中“旧缓冲协议”API 的组成部分。 在 Python 3 中，此
协议已不复存在，但这些函数仍然被公开以便移植 2.x 的代码。 它们被用作
新缓冲协议 的兼容性包装器，但它们并不会在缓冲被导出时向你提供对所获资
源的生命周期控制。

因此，推荐你调用 "PyObject_GetBuffer()" (或者配合 "PyArg_ParseTuple()"
函数族使用 "y*" 或 "w*" 格式码) 来获取一个对象的缓冲视图，并在缓冲视图
可被释放时调用 "PyBuffer_Release()"。

int PyObject_AsCharBuffer(PyObject *obj, const char **buffer, Py_ssize_t *buffer_len)

   返回一个指向可用作基于字符的输入的只读内存地址的指针。 *obj* 参数必
   须支持单段字符缓冲接口。 成功时返回 "0"，将 *buffer* 设为内存地址并
   将 *buffer_len* 设为缓冲区长度。 出错时返回 "-1" 并设置一个
   "TypeError"。

int PyObject_AsReadBuffer(PyObject *obj, const void **buffer, Py_ssize_t *buffer_len)

   返回一个指向包含任意数据的只读内存地址的指针。 *obj* 参数必须支持单
   段可读缓冲接口。 成功时返回 "0"，将 *buffer* 设为内存地址并将
   *buffer_len* 设为缓冲区长度。 出错时返回 "-1" 并设置一个
   "TypeError"。

int PyObject_CheckReadBuffer(PyObject *o)

   如果 *o* 支持单段可读缓冲接口则返回 "1"。 否则返回 "0"。 此函数总是
   会成功执行。

   请注意此函数会尝试获取并释放一个缓冲区，并且在调用对应函数期间发生
   的异常会被屏蔽。 要获取错误报告则应改用 "PyObject_GetBuffer()"。

int PyObject_AsWriteBuffer(PyObject *obj, void **buffer, Py_ssize_t *buffer_len)

   返回一个指向可写内存地址的指针。 *obj* 必须支持单段字符缓冲接口。
   成功时返回 "0"，将 *buffer* 设为内存地址并将 *buffer_len* 设为缓冲
   区长度。 出错时返回 "-1" 并设置一个 "TypeError"。
