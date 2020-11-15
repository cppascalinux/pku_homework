"None" 对象
***********

请注意， "None" 的 "PyTypeObject" 不会直接在 Python / C API 中公开。
由于 "None" 是单例，测试对象标识（在C中使用 "==" ）就足够了。 由于同样
的原因，没有 "PyNone_Check()" 函数。

PyObject* Py_None

   Python "None" 对象，表示缺乏值。 这个对象没有方法。 它需要像引用计
   数一样处理任何其他对象。

Py_RETURN_NONE

   正确处理来自C函数内的 "Py_None" 返回（也就是说，增加 "None" 的引用
   计数并返回它。）
