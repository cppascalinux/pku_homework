在堆中分配对象
**************

PyObject* _PyObject_New(PyTypeObject *type)
    *Return value: New reference.*

PyVarObject* _PyObject_NewVar(PyTypeObject *type, Py_ssize_t size)
    *Return value: New reference.*

PyObject* PyObject_Init(PyObject *op, PyTypeObject *type)
    *Return value: Borrowed reference.*

   为新分配的对象 *op* 初始化它的类型和引用。返回初始化后的对象。如果
   *type* 声明这个对象参与循环垃圾检测，那么这个对象会被添加进垃圾检测
   的对象集中。这个对象的其他字段不会被影响。

PyVarObject* PyObject_InitVar(PyVarObject *op, PyTypeObject *type, Py_ssize_t size)
    *Return value: Borrowed reference.*

   它的功能和 "PyObject_Init()" 一样，并且初始化变量大小的对象的长度。

TYPE* PyObject_New(TYPE, PyTypeObject *type)
    *Return value: New reference.*

   使用 C 结构类型 *TYPE* 和 Python 类型对象 *type* 分配一个新的
   Python 对象。 未在该 Python 对象头中定义的字段不会被初始化；对象的
   引用计数将为一。 内存分配大小由 type 对象的 "tp_basicsize" 字段来确
   定。

TYPE* PyObject_NewVar(TYPE, PyTypeObject *type, Py_ssize_t size)
    *Return value: New reference.*

   使用C的数据结构类型 *TYPE* 和Python的类型对象 *type* 分配一个新的
   Python对象。Python对象头文件中没有定义的字段不会被初始化。被分配的
   内存空间预留了 *TYPE* 结构加 *type* 对象中 "tp_itemsize" 字段提供的
   *size* 字段的值。这对于实现类似元组这种能够在构造期决定自己大小的对
   象是很实用的。将字段的数组嵌入到相同的内存分配中可以减少内存分配的
   次数，这提高了内存分配的效率。

void PyObject_Del(void *op)

   释放由 "PyObject_New()" 或者 "PyObject_NewVar()" 分配内存的对象。这
   通常由对象的type字段定义的 "tp_dealloc" 处理函数来调用。调用这个函
   数以后op对象中的字段都不可以被访问，因为原分配的内存空间已不再是一
   个有效的Python对象。

PyObject _Py_NoneStruct

   像 "None" 一样的Python对象。这个对象仅可以使用 "Py_None" 宏访问，这
   个宏取得指向这个对象的指针。

参见:

  "PyModule_Create()"
     分配内存和创建扩展模块。
