迭代器协议
**********

迭代器有两个函数。

int PyIter_Check(PyObject *o)

   返回 true ， 如果对象 *o* 支持迭代器协议的话。

PyObject* PyIter_Next(PyObject *o)
    *Return value: New reference.*

   返回迭代 *o* 的下一个值。 对象必须是一个迭代器（这应由调用者来判断
   ）。 如果没有余下的值，则返回 "NULL" 并且不设置异常。 如果在获取条
   目时发生了错误，则返回 "NULL" 并且传递异常。

要为迭代器编写一个一个循环，C代码应该看起来像这样

   PyObject *iterator = PyObject_GetIter(obj);
   PyObject *item;

   if (iterator == NULL) {
       /* propagate error */
   }

   while ((item = PyIter_Next(iterator))) {
       /* do something with item */
       ...
       /* release reference when done */
       Py_DECREF(item);
   }

   Py_DECREF(iterator);

   if (PyErr_Occurred()) {
       /* propagate error */
   }
   else {
       /* continue doing useful work */
   }
