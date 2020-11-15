序列协议
********

int PySequence_Check(PyObject *o)

   如果对象提供序列协议，函数返回 "1"，否则返回 "0"。 请注意它将为具有
   "__getitem__()" 方法的 Python 类返回 "1"，除非它们是 "dict" 的子类
   ，因为在一般情况下无法确定它所支持键类型。 此函数总是会成功执行。

Py_ssize_t PySequence_Size(PyObject *o)
Py_ssize_t PySequence_Length(PyObject *o)

   到哪里积分返回序列 *o* 中对象的数量，失败时返回 "-1"。 这相当于
   Python 表达式 "len(o)"。

PyObject* PySequence_Concat(PyObject *o1, PyObject *o2)
    *Return value: New reference.*

   成功时返回 *o1* 和 *o2* 的拼接，失败时返回 "NULL"。 这等价于 Python
   表达式 "o1 + o2"。

PyObject* PySequence_Repeat(PyObject *o, Py_ssize_t count)
    *Return value: New reference.*

   返回序列对象 *o* 重复 *count* 次的结果，失败时返回 "NULL"。 这等价
   于 Python 表达式 "o * count"。

PyObject* PySequence_InPlaceConcat(PyObject *o1, PyObject *o2)
    *Return value: New reference.*

   成功时返回 *o1* 和 *o2* 的拼接，失败时返回 "NULL"。 在 *o1* 支持的
   情况下操作将 *原地* 完成。 这等价于 Python 表达式 "o1 += o2"。

PyObject* PySequence_InPlaceRepeat(PyObject *o, Py_ssize_t count)
    *Return value: New reference.*

   Return the result of repeating sequence object返回序列对象 *o* 重复
   *count* 次的结果，失败时返回 "NULL"。 在 *o* 支持的情况下该操作会 *
   原地* 完成。 这等价于 Python 表达式 "o *= count"。

PyObject* PySequence_GetItem(PyObject *o, Py_ssize_t i)
    *Return value: New reference.*

   返回 *o* 中的第 *i* 号元素，失败时返回 "NULL"。 这等价于 Python 表
   达式 "o[i]"。

PyObject* PySequence_GetSlice(PyObject *o, Py_ssize_t i1, Py_ssize_t i2)
    *Return value: New reference.*

   返回序列对象 *o* 的 *i1* 到 *i2* 的切片，失败时返回 "NULL"。 这等价
   于 Python 表达式 "o[i1:i2]"。

int PySequence_SetItem(PyObject *o, Py_ssize_t i, PyObject *v)

   将对象 *v* 赋值给 *o* 的第 *i* 号元素。 失败时会引发异常并返回 "-1"
   ；成功时返回 "0"。 这相当于 Python 语句 "o[i] = v"。 此函数 *不会*
   改变对 *v* 的引用。

   如果 *v* 为 "NULL"，元素将被删除，但是此特性已被弃用，应当改用
   "PySequence_DelItem()"。

int PySequence_DelItem(PyObject *o, Py_ssize_t i)

   删除对象 *o* 的第 *i* 号元素。 失败时返回 "-1"。 这相当于 Python 语
   句 "del o[i]"。

int PySequence_SetSlice(PyObject *o, Py_ssize_t i1, Py_ssize_t i2, PyObject *v)

   将序列对象 *v* 赋值给序列对象 *o* 的从 *i1* 到 *i2* 切片。 这相当于
   Python 语句 "o[i1:i2] = v"。

int PySequence_DelSlice(PyObject *o, Py_ssize_t i1, Py_ssize_t i2)

   删除序列对象 *o* 的从 *i1* 到 *i2* 的切片。 失败时返回 "-1"。 这相
   当于 Python 语句 "del o[i1:i2]"。

Py_ssize_t PySequence_Count(PyObject *o, PyObject *value)

   返回 *value* 在 *o* 中出现的次数，即返回使得 "o[key] == value" 的键
   的数量。 失败时返回 "-1"。 这相当于 Python 表达式 "o.count(value)"
   。

int PySequence_Contains(PyObject *o, PyObject *value)

   确定 *o* 是否包含 *value*。 如果 *o* 中的某一项等于 *value*，则返回
   "1"，否则返回 "0"。 出错时，返回 "-1"。 这相当于 Python 表达式
   "value in o"。

Py_ssize_t PySequence_Index(PyObject *o, PyObject *value)

   返回第一个索引*i*,其中 "o[i] == value".出错时,返回“-1”.相当于Python
   的``o.index(value)``表达式.

PyObject* PySequence_List(PyObject *o)
    *Return value: New reference.*

   返回一个列表对象，其内容与序列或可迭代对象 *o* 相同，失败时返回
   "NULL"。 返回的列表保证是一个新对象。 这等价于 Python 表达式
   "list(o)"。

PyObject* PySequence_Tuple(PyObject *o)
    *Return value: New reference.*

   返回一个元组对象，其内容与序列或可迭代对象 *o* 相同，失败时返回
   "NULL"。 如果 *o* 为元组，则将返回一个新的引用，在其他情况下将使用
   适当的内容构造一个元组。 这等价于 Python 表达式 "tuple(o)"。

PyObject* PySequence_Fast(PyObject *o, const char *m)
    *Return value: New reference.*

   将序列或可迭代对象 *o* 作为其他 "PySequence_Fast*" 函数族可用的对象
   返回。 如果该对象不是序列或可迭代对象，则会引发 "TypeError" 并将
   *m* 作为消息文本。 失败时返回 "NULL"。

   "PySequence_Fast*" 函数之所以这样命名，是因为它们会假定 *o* 是一个
   "PyTupleObject" 或 "PyListObject" 并直接访问 *o* 的数据字段。

   作为 CPython 的实现细节，如果 *o* 已经是一个序列或列表，它将被直接
   返回。

Py_ssize_t PySequence_Fast_GET_SIZE(PyObject *o)

   在 *o* 由 "PySequence_Fast()" 返回且 *o* 不为 "NULL" 的情况下返回
   *o* 的长度。 也可以通过在 *o* 上调用 "PySequence_Size()" 来获取大小
   ，但是 "PySequence_Fast_GET_SIZE()" 速度更快，因为它可以假定 *o* 为
   列表或元组。

PyObject* PySequence_Fast_GET_ITEM(PyObject *o, Py_ssize_t i)
    *Return value: Borrowed reference.*

   在 *o* 由 "PySequence_Fast()" 返回且 *o* 不 "NULL"，并且 *i* d在索
   引范围内的情况下返回 *o* 的第 *i* 号元素。

PyObject** PySequence_Fast_ITEMS(PyObject *o)

   返回 PyObject 指针的底层数组。 假设 *o* 由 "PySequence_Fast()" 返回
   且 *o* 不为 "NULL"。

   请注意,如果列表调整大小,重新分配可能会重新定位items数组.因此,仅在序
   列无法更改的上下文中使用基础数组指针.

PyObject* PySequence_ITEM(PyObject *o, Py_ssize_t i)
    *Return value: New reference.*

   返回 *o* 的第 *i* 个元素或在失败时返回 "NULL"。 此形式比
   "PySequence_GetItem()" 理馔，但不会检查 *o* 上的
   "PySequence_Check()" 是否为真值，也不会对负序号进行调整。
