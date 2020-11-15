协程对象
********

3.5 新版功能.

协程对象是使用 "async" 关键字声明的函数返回的。

PyCoroObject

   用于协程对象的C结构体。

PyTypeObject PyCoro_Type

   与协程对象对应的类型对​​象。

int PyCoro_CheckExact(PyObject *ob)

   如果 *ob* 的类型是 "PyCoro_Type" 则返回真值；*ob* 必须不为 "NULL"。

PyObject* PyCoro_New(PyFrameObject *frame, PyObject *name, PyObject *qualname)
    *Return value: New reference.*

   基于 *frame* 对象创建并返回一个新的协程对象，其中 "__name__" 和
   "__qualname__" 设为 *name* 和 *qualname*。 此函数会取得一个对
   *frame* 的引用。 *frame* 参数必须不为 "NULL"。
