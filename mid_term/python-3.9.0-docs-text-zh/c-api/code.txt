代码对象
********

代码对象是 CPython 实现的低级细节。 每个代表一块尚未绑定到函数中的可执
行代码。

PyCodeObject

   用于描述代码对象的对象的 C 结构。 此类型字段可随时更改。

PyTypeObject PyCode_Type

   这是一个 "PyTypeObject" 实例，其表示Python的 "code" 类型。

int PyCode_Check(PyObject *co)

   如果 *co* 是一个 "code" 对象则返回 true。

int PyCode_GetNumFree(PyCodeObject *co)

   返回 *co* 中的自由变量数。

PyCodeObject* PyCode_New(int argcount, int kwonlyargcount, int nlocals, int stacksize, int flags, PyObject *code, PyObject *consts, PyObject *names, PyObject *varnames, PyObject *freevars, PyObject *cellvars, PyObject *filename, PyObject *name, int firstlineno, PyObject *lnotab)
    *Return value: New reference.*

   返回一个新的代码对象。 如果你需要一个虚拟代码对象来创建一个代码帧，
   请使用 "PyCode_NewEmpty()"。 调用 "PyCode_New()" 直接可以绑定到准确
   的 Python 版本，因为字节码的定义经常变化。

PyCodeObject* PyCode_NewWithPosOnlyArgs(int argcount, int posonlyargcount, int kwonlyargcount, int nlocals, int stacksize, int flags, PyObject *code, PyObject *consts, PyObject *names, PyObject *varnames, PyObject *freevars, PyObject *cellvars, PyObject *filename, PyObject *name, int firstlineno, PyObject *lnotab)
    *Return value: New reference.*

   类似于 "PyCode_New()"，但带有一个额外的 "posonlyargcount" 用于仅限
   位置参数。

   3.8 新版功能.

PyCodeObject* PyCode_NewEmpty(const char *filename, const char *funcname, int firstlineno)
    *Return value: New reference.*

   返回具有指定文件名、函数名和第一行号的新空代码对象。 对于 "exec()"
   或 "eval()" 生成的代码对象是非法的。
