生成器对象
**********

生成器对象是Python用来实现生成器迭代器的对象。它们通常通过迭代产生值的
函数来创建，而不是显式调用 "PyGen_New()" 或 "PyGen_NewWithQualName()"
。

PyGenObject

   用于生成器对象的C结构体。

PyTypeObject PyGen_Type

   与生成器对象对应的类型对​​象。

int PyGen_Check(PyObject *ob)

   如果 *ob* 是一个生成器对象则返回真值；*ob* 必须不为 "NULL"。

int PyGen_CheckExact(PyObject *ob)

   如果 *ob* 的类型为 "PyGen_Type" 则返回真值；*ob* 必须不为 "NULL"。

PyObject* PyGen_New(PyFrameObject *frame)
    *Return value: New reference.*

   基于 *frame* 对象创建并返回一个新的生成器对象。 此函数会取走一个对
   *frame* 的引用。 参数必须不为 "NULL"。

PyObject* PyGen_NewWithQualName(PyFrameObject *frame, PyObject *name, PyObject *qualname)
    *Return value: New reference.*

   基于 *frame* 对象创建并返回一个新的生成器对象，其中 "__name__" 和
   "__qualname__" 设为 *name* 和 *qualname*。 此函数会取走一个对
   *frame* 的引用。 *frame* 参数必须不为 "NULL"。
