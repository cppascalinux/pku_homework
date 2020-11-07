Cell 对象
*********

“Cell”对象用于实现由多个作用域引用的变量。 对于每个这样的变量，一个
“Cell”对象为了存储该值而被创建；引用该值的每个堆栈框架的局部变量包含同
样使用该变量的对外部作用域的“Cell”引用。 访问该值时，将使用“Cell”中包
含的值而不是单元格对象本身。 这种对“Cell”对象的非关联化的引用需要支持
生成的字节码；访问时不会自动非关联化这些内容。 “Cell”对象在其他地方可
能不太有用。

PyCellObject

   用于Cell对象的C结构体。

PyTypeObject PyCell_Type

   与 Cell 对象对应的类型对​​象。

int PyCell_Check(ob)

   如果 *ob* 是一个 cell 对象则返回真值；*ob* 必须不为 "NULL"。

PyObject* PyCell_New(PyObject *ob)
    *Return value: New reference.*

   创建并返回一个包含值 *ob* 的新 cell 对象。形参可以为 "NULL"。

PyObject* PyCell_Get(PyObject *cell)
    *Return value: New reference.*

   返回 cell 对象 *cell* 的内容。

PyObject* PyCell_GET(PyObject *cell)
    *Return value: Borrowed reference.*

   返回 cell 对象 *cell* 的内容，但是不检测 *cell* 是否非 "NULL" 并且
   为一个 cell 对象。

int PyCell_Set(PyObject *cell, PyObject *value)

   将 cell 对象 *cell* 的内容设为 *value*。 这将释放任何对 cell 对象当
   前内容的引用。 *value* 可以为 "NULL"。 *cell* 必须为非 "NULL"；如果
   它不是一个 cell 对象则将返回 "-1"。 如果设置成功则将返回 "0"。

void PyCell_SET(PyObject *cell, PyObject *value)

   将 cell 对象 *cell* 的值设为 *value*。 不会调整引用计数，并且不会进
   行检测以保证安全；*cell* 必须为非 "NULL" 并且为一个 cell 对象。
