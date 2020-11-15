弱引用对象
**********

Python 支持 “弱引用” 作为一类对象。具体来说，有两种直接实现弱引用的对
象。第一种就是简单的引用对象，第二种尽可能地作用为一个原对象的代理。

int PyWeakref_Check(ob)

   如果 “ob” 是一个引用或者一个代理对象，则返回一个 true。

int PyWeakref_CheckRef(ob)

   如果 “ob” 是一个引用，则返回 true。

int PyWeakref_CheckProxy(ob)

   如果 “ob” 是一个代理对象，则返回 true。

PyObject* PyWeakref_NewRef(PyObject *ob, PyObject *callback)
    *Return value: New reference.*

   返回对象 *ob* 的一个弱引用对象。 该函数总是会返回一个新的引用，但不
   保证创建一个新的对象；它有可能返回一个现有的引用对象。 第二个形参
   *callback* 为一个可调用对象，它会在 *ob* 被作为垃圾回收时接收通知；
   它应该接受一个单独形参，即弱引用对象本身。 *callback* 也可以为
   "None" 或 "NULL"。 如果 *ob* 不是一个弱引用对象，或者如果
   *callback* 不是可调用对象，"None" 或 "NULL"，该函数将返回 "NULL" 并
   且引发 "TypeError"。

PyObject* PyWeakref_NewProxy(PyObject *ob, PyObject *callback)
    *Return value: New reference.*

   返回对象 *ob* 的一个弱引用代理对象。 该函数将总是返回一个新的引用，
   但不保证创建一个新的对象；它有可能返回一个现有的代理对象。 第二个形
   参 *callback* 为一个可调用对象，它会在 *ob* 被作为垃圾回收时接收通
   知；它应该接受一个单独形参，即弱引用对象本身。 *callback* 也可以为
   "None" 或 "NULL"。 如果 *ob* 不是一个弱引用对象，或者如果
   *callback* 不是可调用对象，"None" 或 "NULL"，该函数将返回 "NULL" 并
   且引发 "TypeError"。

PyObject* PyWeakref_GetObject(PyObject *ref)
    *Return value: Borrowed reference.*

   返回弱引用对象 ref 的被引用对象。如果被引用对象不再存在，则返回
   "Py_None"。

   注解:

     该函数返回被引用对象的一个**借来的引用**。这意味着除非你很清楚在
     你使用期间这个对象不可能被销毁，否则你应该始终对该对象调用
     "Py_INCREF()"。

PyObject* PyWeakref_GET_OBJECT(PyObject *ref)
    *Return value: Borrowed reference.*

   类似 "PyWeakref_GetObject()"，但实现为一个不做类型检查的宏。
