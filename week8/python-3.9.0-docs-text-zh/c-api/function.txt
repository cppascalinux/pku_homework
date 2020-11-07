函数对象
********

有一些特定于 Python 函数的函数。

PyFunctionObject

   用于函数的 C 结构体。

PyTypeObject PyFunction_Type

   这是一个 "PyTypeObject" 实例并表示 Python 函数类型。 它作为
   "types.FunctionType" 向 Python 程序员公开。

int PyFunction_Check(PyObject *o)

   如果 *o* 是函数对象 (类型为 "PyFunction_Type") 则返回真值。 形参必
   须不为 "NULL"。

PyObject* PyFunction_New(PyObject *code, PyObject *globals)
    *Return value: New reference.*

   返回与代码对象 *code* 关联的新函数对象。 *globals* 必须是一个字典，
   该函数可以访问全局变量。

   从代码对象中提取函数的文档字符串和名称。 *__module__* 会从
   *globals* 中提取。 参数 defaults, annotations 和 closure 设为
   "NULL"。 *__qualname__* 设为与函数名称相同的值。

PyObject* PyFunction_NewWithQualName(PyObject *code, PyObject *globals, PyObject *qualname)
    *Return value: New reference.*

   类似 "PyFunction_New()"，但还允许设置函数对象的 "__qualname__" 属性
   。 *qualname* 应当是 unicode 对象或 "NULL"；如果是 "NULL" 则
   "__qualname__" 属性设为与其 "__name__" 属性相同的值。

   3.3 新版功能.

PyObject* PyFunction_GetCode(PyObject *op)
    *Return value: Borrowed reference.*

   返回与函数对象 *op* 关联的代码对象。

PyObject* PyFunction_GetGlobals(PyObject *op)
    *Return value: Borrowed reference.*

   返回与函数对象*op*相关联的全局字典。

PyObject* PyFunction_GetModule(PyObject *op)
    *Return value: Borrowed reference.*

   返回函数对象 *op* 的 *__module__* 属性，通常为一个包含了模块名称的
   字符串，但可以通过 Python 代码设为返回其他任意对象。

PyObject* PyFunction_GetDefaults(PyObject *op)
    *Return value: Borrowed reference.*

   返回函数对象 *op* 的参数默认值。 这可以是一个参数元组或 "NULL"。

int PyFunction_SetDefaults(PyObject *op, PyObject *defaults)

   为函数对象 *op* 设置参数默认值。 *defaults* 必须为 "Py_None" 或一个
   元组。

   失败时引发 "SystemError" 异常并返回 "-1" 。

PyObject* PyFunction_GetClosure(PyObject *op)
    *Return value: Borrowed reference.*

   返回关联到函数对象 *op* 的闭包。 这可以是 "NULL" 或 cell 对象的元组
   。

int PyFunction_SetClosure(PyObject *op, PyObject *closure)

   设置关联到函数对象 *op* 的闭包。 *closure* 必须为 "Py_None" 或 cell
   对象的元组。

   失败时引发 "SystemError" 异常并返回 "-1" 。

PyObject *PyFunction_GetAnnotations(PyObject *op)
    *Return value: Borrowed reference.*

   返回函数对象 *op* 的标注。 这可以是一个可变字典或 "NULL"。

int PyFunction_SetAnnotations(PyObject *op, PyObject *annotations)

   设置函数对象 *op* 的标注。 *annotations* 必须为一个字典或 "Py_None"
   。

   失败时引发 "SystemError" 异常并返回 "-1" 。
