MemoryView 对象
***************

一个 "memoryview" 对象C级别的 缓冲区接口 暴露为一个可以像任何其他对象
一样传递的 Python 对象。

PyObject *PyMemoryView_FromObject(PyObject *obj)
    *Return value: New reference.*

   从提供缓冲区接口的对象创建 memoryview 对象。 如果 *obj* 支持可写缓
   冲区导出，则 memoryview 对象将可以被读/写，否则它可能是只读的，也可
   以是导出器自行决定的读/写。

PyObject *PyMemoryView_FromMemory(char *mem, Py_ssize_t size, int flags)
    *Return value: New reference.*

   使用 *mem* 作为底层缓冲区创建一个 memoryview 对象。 *flags* 可以是
   "PyBUF_READ" 或者 "PyBUF_WRITE" 之一.

   3.3 新版功能.

PyObject *PyMemoryView_FromBuffer(Py_buffer *view)
    *Return value: New reference.*

   创建一个包含给定缓冲区结构 *view* 的 memoryview 对象。 对于简单的字
   节缓冲区，"PyMemoryView_FromMemory()" 是首选函数。

PyObject *PyMemoryView_GetContiguous(PyObject *obj, int buffertype, char order)
    *Return value: New reference.*

   从定义缓冲区接口的对象创建一个 memoryview 对象 *contiguous* 内存块
   （在 'C' 或 'F'ortran *order* 中）。 如果内存是连续的，则
   memoryview 对象指向原始内存。 否则，复制并且 memoryview 指向新的
   bytes 对象。

int PyMemoryView_Check(PyObject *obj)

   如果对象 *obj* 是 memoryview 对象，则返回 true 。 目前不允许创建
   "memoryview" 的子类。

Py_buffer *PyMemoryView_GET_BUFFER(PyObject *mview)

   返回指向 memoryview 的导出缓冲区私有副本的指针。 *mview* **必须**
   是一个 memoryview 实例；这个宏不检查它的类型，你必须自己检查，否则
   你将面临崩溃风险。

Py_buffer *PyMemoryView_GET_BASE(PyObject *mview)

   返回 memoryview 所基于的导出对象的指针，或者如果 memoryview 已由函
   数 "PyMemoryView_FromMemory()" 或 "PyMemoryView_FromBuffer()" 创建
   则返回 "NULL"。 *mview* **必须** 是一个 memoryview 实例。
