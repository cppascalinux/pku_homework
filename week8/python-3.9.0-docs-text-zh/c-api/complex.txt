复数对象
********

从C API看，Python的复数对象由两个不同的部分实现：一个是在Python程序使
用的Python对象，另外的是一个代表真正复数值的C结构体。API提供了函数共同
操作两者。


表示复数的C结构体
=================

需要注意的是接受这些结构体的作为参数并当做结果返回的函数，都是传递“值”
而不是引用指针。此规则适用于整个API。

Py_complex

   这是一个对应Python复数对象的值部分的C结构体。绝大部分处理复数对象的
   函数都用这类型的结构体作为输入或者输出值，它可近似地定义为：

      typedef struct {
         double real;
         double imag;
      } Py_complex;

Py_complex _Py_c_sum(Py_complex left, Py_complex right)

   返回两个复数的和，用 C 类型 "Py_complex" 表示。

Py_complex _Py_c_diff(Py_complex left, Py_complex right)

   返回两个复数的差，用 C 类型 "Py_complex" 表示。

Py_complex _Py_c_neg(Py_complex complex)

   返回复数 *complex* 的负值，用 C 类型 "Py_complex" 表示。

Py_complex _Py_c_prod(Py_complex left, Py_complex right)

   返回两个复数的乘积，用 C 类型 "Py_complex" 表示。

Py_complex _Py_c_quot(Py_complex dividend, Py_complex divisor)

   返回两个复数的商，用 C 类型 "Py_complex" 表示。

   如果 *divisor* 为空，这个方法返回零并设置 "errno" 为 "EDOM"。

Py_complex _Py_c_pow(Py_complex num, Py_complex exp)

   返回 *num* 的 *exp* 次幂，用 C 类型 "Py_complex" 表示。

   如果 *num* 为空且 *exp* 不是正实数，这个方法返回零并设置 "errno" 为
   "EDOM"。


表示复数的Python对象
====================

PyComplexObject

   这个C类型 "PyObject" 的子类型代表一个 Python 复数对象。

PyTypeObject PyComplex_Type

   这是个属于C类型 "PyTypeObject" 的代表 Python 复数类型的实例。 和
   Python 层面的类 "complex" 是同一个对象。

int PyComplex_Check(PyObject *p)

   如果它的参数是一个C类型 "PyComplexObject" 或者是C类型
   "PyComplexObject" 的子类型，返回真。

int PyComplex_CheckExact(PyObject *p)

   如果它的参数是一个C类型 "PyComplexObject" 但不是C类型
   "PyComplexObject" 的子类型，返回真。

PyObject* PyComplex_FromCComplex(Py_complex v)
    *Return value: New reference.*

   根据C类型 "Py_complex" 的值生成一个新的Python复数对象。

PyObject* PyComplex_FromDoubles(double real, double imag)
    *Return value: New reference.*

   根据 *real* 和 *imag* 返回一个新的C类型 "PyComplexObject" 对象。

double PyComplex_RealAsDouble(PyObject *op)

   以C类型 "double" 返回 *op* 的实部。

double PyComplex_ImagAsDouble(PyObject *op)

   以C类型 "double" 返回 *op* 的虚部。

Py_complex PyComplex_AsCComplex(PyObject *op)

   返回复数 *op* 的C类型 "Py_complex" 值。

   如果 *op* 不是一个 Python 复数对象，但是具有 "__complex__()" 方法，
   此方法将首先被调用，将 *op* 转换为一个 Python 复数对象。 如果
   "__complex__()" 未定义则将回退至 "__float__()"，如果 "__float__()"
   未定义则将回退至 "__index__()"。 如果失败，此方法将返回 "-1.0" 作为
   实数值。

   在 3.8 版更改: 如果可用将使用 "__index__()"。
