映射协议
********

参见 "PyObject_GetItem()"、"PyObject_SetItem()" 与
"PyObject_DelItem()"。

int PyMapping_Check(PyObject *o)

   如果对象提供映射协议或支持切片则返回 "1"，否则返回 "0"。 请注意它将
   为具有 "__getitem__()" 方法的 Python 类返回 "1"，因为在一般情况下无
   法确定它所支持的键类型。 此函数总是会成功执行。

Py_ssize_t PyMapping_Size(PyObject *o)
Py_ssize_t PyMapping_Length(PyObject *o)

   成功时返回对象 *o* 中键的数量，失败时返回 "-1"。 这相当于 Python 表
   达式 "len(o)"。

PyObject* PyMapping_GetItemString(PyObject *o, const char *key)
    *Return value: New reference.*

   返回 *o* 中对应于字符串 *key* 的元素，或者失败时返回 "NULL"。 这相
   当于 Python 表达式 "o[key]"。 另请参见 also "PyObject_GetItem()"。

int PyMapping_SetItemString(PyObject *o, const char *key, PyObject *v)

   在对象 *o* 中将字符串 *key* 映射到值 *v*。 失败时返回 "-1"。 这相当
   于 Python 语句 "o[key] = v"。 另请参见 "PyObject_SetItem()"。 此函
   数 *不会* 增加对 *v* 的引用。

int PyMapping_DelItem(PyObject *o, PyObject *key)

   从对象 *o* 中移除对象 *key* 的映射。 失败时返回 "-1"。 这相当于
   Python 语句 "del o[key]"。 这是 "PyObject_DelItem()" 的一个别名。

int PyMapping_DelItemString(PyObject *o, const char *key)

   从对象 *o* 中移除字符串 *key* 的映射。 失败时返回 "-1"。 这相当于
   Python 语句 "del o[key]"。

int PyMapping_HasKey(PyObject *o, PyObject *key)

   如果映射对象具有键 *key* 则返回 "1"，否则返回 "0"。 这相当于 Python
   表达式 "key in o"。 此函数总是会成功执行。

   请注意在调用 "__getitem__()" 方法期间发生的异常将会被屏蔽。 要获取
   错误报告请改用 "PyObject_GetItem()"。

int PyMapping_HasKeyString(PyObject *o, const char *key)

   如果映射对象具有键 *key* 则返回 "1"，否则返回 "0"。 这相当于 Python
   表达式 "key in o"。 此函数总是会成功执行。

   请注意在调用 "__getitem__()" 方法期间发生的异常将会被屏蔽。 要获取
   错误报告请改用 "PyMapping_GetItemString()"。

PyObject* PyMapping_Keys(PyObject *o)
    *Return value: New reference.*

   成功时，返回对象 *o* 中的键的列表。 失败时，返回 "NULL"。

   在 3.7 版更改: 在之前版本中，此函数返回一个列表或元组。

PyObject* PyMapping_Values(PyObject *o)
    *Return value: New reference.*

   成功时，返回对象 *o* 中的值的列表。 失败时，返回 "NULL"。

   在 3.7 版更改: 在之前版本中，此函数返回一个列表或元组。

PyObject* PyMapping_Items(PyObject *o)
    *Return value: New reference.*

   成功时，返回对象 *o* 中条目的列表，其中每个条目是一个包含键值对的元
   组。 失败时，返回 "NULL"。

   在 3.7 版更改: 在之前版本中，此函数返回一个列表或元组。
