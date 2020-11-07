"operator" --- 标准运算符替代函数
*********************************

**源代码:** Lib/operator.py

======================================================================

"operator" 模块提供了一套与Python的内置运算符对应的高效率函数。例如，
"operator.add(x, y)" 与表达式 "x+y" 相同。 许多函数名与特殊方法名相同
，只是没有双下划线。为了向后兼容性，也保留了许多包含双下划线的函数。为
了表述清楚，建议使用没有双下划线的函数。

函数包含的种类有：对象的比较运算、逻辑运算、数学运算以及序列运算。

对象比较函数适用于所有的对象，函数名根据它们对应的比较运算符命名。

operator.lt(a, b)
operator.le(a, b)
operator.eq(a, b)
operator.ne(a, b)
operator.ge(a, b)
operator.gt(a, b)
operator.__lt__(a, b)
operator.__le__(a, b)
operator.__eq__(a, b)
operator.__ne__(a, b)
operator.__ge__(a, b)
operator.__gt__(a, b)

   在 *a* 和 *b* 之间进行全比较。具体的，"lt(a, b)" 与 "a < b" 相同，
   "le(a, b)" 与 "a <= b" 相同，"eq(a, b)" 与 "a == b" 相同，"ne(a,
   b)" 与 "a != b" 相同，"gt(a, b)" 与 "a > b" 相同，"ge(a, b)``与 ``a
   >= b" 相同。注意这些函数可以返回任何值，无论它是否可当作布尔值。关
   于全比较的更多信息请参考 比较运算 。

逻辑运算通常也适用于所有对象，并且支持真值检测、标识检测和布尔运算：

operator.not_(obj)
operator.__not__(obj)

   返回 "not" *obj* 的结果。 （请注意对象实例并没有 "__not__()" 方法；
   只有解释器核心可定义此操作。 结果会受 "__bool__()" 和 "__len__()"
   方法影响。）

operator.truth(obj)

   如果 *obj* 为真值则返回 "True"，否则返回 "False"。 这等价于使用
   "bool" 构造器。

operator.is_(a, b)

   返回 "a is b"。 检测对象标识。

operator.is_not(a, b)

   返回 "a is not b"。 检测对象标识。

数学和按位运算的种类是最多的：

operator.abs(obj)
operator.__abs__(obj)

   返回 *obj* 的绝对值。

operator.add(a, b)
operator.__add__(a, b)

   对于数字 *a* 和 *b*，返回 "a + b"。

operator.and_(a, b)
operator.__and__(a, b)

   返回 *x* 和 *y* 按位与的结果。

operator.floordiv(a, b)
operator.__floordiv__(a, b)

   返回 "a // b"。

operator.index(a)
operator.__index__(a)

   返回 *a* 转换为整数的结果。 等价于 "a.__index__()"。

operator.inv(obj)
operator.invert(obj)
operator.__inv__(obj)
operator.__invert__(obj)

   返回数字 *obj* 按位取反的结果。 这等价于 "~obj"。

operator.lshift(a, b)
operator.__lshift__(a, b)

   返回 *a* 左移 *b* 位的结果。

operator.mod(a, b)
operator.__mod__(a, b)

   返回 "a % b"。

operator.mul(a, b)
operator.__mul__(a, b)

   对于数字 *a* 和 *b*，返回 "a * b"。

operator.matmul(a, b)
operator.__matmul__(a, b)

   返回 "a @ b"。

   3.5 新版功能.

operator.neg(obj)
operator.__neg__(obj)

   返回 *obj* 取负的结果 ("-obj")。

operator.or_(a, b)
operator.__or__(a, b)

   返回 *a* 和 *b* 按位或的结果。

operator.pos(obj)
operator.__pos__(obj)

   返回 *obj* 取正的结果 ("+obj")。

operator.pow(a, b)
operator.__pow__(a, b)

   对于数字 *a* 和 *b*，返回 "a ** b"。

operator.rshift(a, b)
operator.__rshift__(a, b)

   返回 *a* 右移 *b* 位的结果。

operator.sub(a, b)
operator.__sub__(a, b)

   返回 "a - b"。

operator.truediv(a, b)
operator.__truediv__(a, b)

   返回 "a / b" 例如 2/3 将等于 .66 而不是 0。 这也被称为“真”除法。

operator.xor(a, b)
operator.__xor__(a, b)

   返回 *a* 和 *b* 按位异或的结果。

适用于序列的操作（其中一些也适用于映射）包括：

operator.concat(a, b)
operator.__concat__(a, b)

   对于序列 *a* 和 *b*，返回 "a + b"。

operator.contains(a, b)
operator.__contains__(a, b)

   返回 "b in a" 检测的结果。 请注意操作数是反序的。

operator.countOf(a, b)

   返回 *b* 在 *a* 中的出现次数。

operator.delitem(a, b)
operator.__delitem__(a, b)

   移除索引号 *b* 上的值 *a*。

operator.getitem(a, b)
operator.__getitem__(a, b)

   返回索引号 *b* 上的值 *a*。

operator.indexOf(a, b)

   返回 *b* 在 *a* 中首次出现所在的索引号。

operator.setitem(a, b, c)
operator.__setitem__(a, b, c)

   将索引号 *b* 上的值 *a* 设为 *c*。

operator.length_hint(obj, default=0)

   返回对象 *o* 的估计长度。 首先尝试返回其实际长度，再使用
   "object.__length_hint__()" 得出估计值，最后返回默认值。

   3.4 新版功能.

"operator" 模块还定义了一些用于常规属性和条目查找的工具。 这些工具适合
用来编写快速字段提取器作为 "map()", "sorted()", "itertools.groupby()"
或其他需要相应函数参数的函数的参数。

operator.attrgetter(attr)
operator.attrgetter(*attrs)

   返回一个可从操作数中获取 *attr* 的可调用对象。 如果请求了一个以上的
   属性，则返回一个属性元组。 属性名称还可包含点号。 例如：

   * 在 "f = attrgetter('name')" 之后，调用 "f(b)" 将返回 "b.name"。

   * 在 "f = attrgetter('name', 'date')" 之后，调用 "f(b)" 将返回
     "(b.name, b.date)"。

   * 在 "f = attrgetter('name.first', 'name.last')" 之后，调用 "f(b)"
     将返回 "(b.name.first, b.name.last)"。

   等价于:

      def attrgetter(*items):
          if any(not isinstance(item, str) for item in items):
              raise TypeError('attribute name must be a string')
          if len(items) == 1:
              attr = items[0]
              def g(obj):
                  return resolve_attr(obj, attr)
          else:
              def g(obj):
                  return tuple(resolve_attr(obj, attr) for attr in items)
          return g

      def resolve_attr(obj, attr):
          for name in attr.split("."):
              obj = getattr(obj, name)
          return obj

operator.itemgetter(item)
operator.itemgetter(*items)

   返回一个使用操作数的 "__getitem__()" 方法从操作数中获取 *item* 的可
   调用对象。 如果指定了多个条目，则返回一个查找值的元组。 例如：

   * 在 "f = itemgetter(2)" 之后，调用 "f(r)" 将返回 "r[2]"。

   * 在 "g = itemgetter(2, 5, 3)" 之后，调用 "g(r)" 将返回 "(r[2],
     r[5], r[3])"。

   等价于:

      def itemgetter(*items):
          if len(items) == 1:
              item = items[0]
              def g(obj):
                  return obj[item]
          else:
              def g(obj):
                  return tuple(obj[item] for item in items)
          return g

   传入的条目可以为操作数的 "__getitem__()" 所接受的任何类型。 字典接
   受任意可哈希的值。 列表、元组和字符串接受 index 或 slice 对象：

   >>> itemgetter('name')({'name': 'tu', 'age': 18})
   'tu'
   >>> itemgetter(1)('ABCDEFG')
   'B'
   >>> itemgetter(1,3,5)('ABCDEFG')
   ('B', 'D', 'F')
   >>> itemgetter(slice(2,None))('ABCDEFG')
   'CDEFG'

   >>> soldier = dict(rank='captain', name='dotterbart')
   >>> itemgetter('rank')(soldier)
   'captain'

   使用 "itemgetter()" 从元组的记录中提取特定字段的例子：

   >>> inventory = [('apple', 3), ('banana', 2), ('pear', 5), ('orange', 1)]
   >>> getcount = itemgetter(1)
   >>> list(map(getcount, inventory))
   [3, 2, 5, 1]
   >>> sorted(inventory, key=getcount)
   [('orange', 1), ('banana', 2), ('apple', 3), ('pear', 5)]

operator.methodcaller(name, /, *args, **kwargs)

   返回一个在操作数上调用 *name* 方法的可调用对象。 如果给出额外的参数
   和/或关键字参数，它们也将被传给该方法。 例如：

   * 在 "f = methodcaller('name')" 之后，调用 "f(b)" 将返回 "b.name()"
     。

   * 在 "f = methodcaller('name', 'foo', bar=1)" 之后，调用 "f(b)" 将
     返回 "b.name('foo', bar=1)"。

   等价于:

      def methodcaller(name, /, *args, **kwargs):
          def caller(obj):
              return getattr(obj, name)(*args, **kwargs)
          return caller


将运算符映射到函数
==================

以下表格显示了抽象运算是如何对应于 Python 语法中的运算符和 "operator"
模块中的函数的。

+-------------------------+---------------------------+-----------------------------------------+
| 运算                    | 语法                      | 函数                                    |
|=========================|===========================|=========================================|
| 加法                    | "a + b"                   | "add(a, b)"                             |
+-------------------------+---------------------------+-----------------------------------------+
| 字符串拼接              | "seq1 + seq2"             | "concat(seq1, seq2)"                    |
+-------------------------+---------------------------+-----------------------------------------+
| 包含测试                | "obj in seq"              | "contains(seq, obj)"                    |
+-------------------------+---------------------------+-----------------------------------------+
| 除法                    | "a / b"                   | "truediv(a, b)"                         |
+-------------------------+---------------------------+-----------------------------------------+
| 除法                    | "a // b"                  | "floordiv(a, b)"                        |
+-------------------------+---------------------------+-----------------------------------------+
| 按位与                  | "a & b"                   | "and_(a, b)"                            |
+-------------------------+---------------------------+-----------------------------------------+
| 按位异或                | "a ^ b"                   | "xor(a, b)"                             |
+-------------------------+---------------------------+-----------------------------------------+
| 按位取反                | "~ a"                     | "invert(a)"                             |
+-------------------------+---------------------------+-----------------------------------------+
| 按位或                  | "a | b"                   | "or_(a, b)"                             |
+-------------------------+---------------------------+-----------------------------------------+
| 取幂                    | "a ** b"                  | "pow(a, b)"                             |
+-------------------------+---------------------------+-----------------------------------------+
| 标识                    | "a is b"                  | "is_(a, b)"                             |
+-------------------------+---------------------------+-----------------------------------------+
| 标识                    | "a is not b"              | "is_not(a, b)"                          |
+-------------------------+---------------------------+-----------------------------------------+
| 索引赋值                | "obj[k] = v"              | "setitem(obj, k, v)"                    |
+-------------------------+---------------------------+-----------------------------------------+
| 索引删除                | "del obj[k]"              | "delitem(obj, k)"                       |
+-------------------------+---------------------------+-----------------------------------------+
| 索引取值                | "obj[k]"                  | "getitem(obj, k)"                       |
+-------------------------+---------------------------+-----------------------------------------+
| 左移                    | "a << b"                  | "lshift(a, b)"                          |
+-------------------------+---------------------------+-----------------------------------------+
| 取模                    | "a % b"                   | "mod(a, b)"                             |
+-------------------------+---------------------------+-----------------------------------------+
| 乘法                    | "a * b"                   | "mul(a, b)"                             |
+-------------------------+---------------------------+-----------------------------------------+
| 矩阵乘法                | "a @ b"                   | "matmul(a, b)"                          |
+-------------------------+---------------------------+-----------------------------------------+
| 取反（算术）            | "- a"                     | "neg(a)"                                |
+-------------------------+---------------------------+-----------------------------------------+
| 取反（逻辑）            | "not a"                   | "not_(a)"                               |
+-------------------------+---------------------------+-----------------------------------------+
| 正数                    | "+ a"                     | "pos(a)"                                |
+-------------------------+---------------------------+-----------------------------------------+
| 右移                    | "a >> b"                  | "rshift(a, b)"                          |
+-------------------------+---------------------------+-----------------------------------------+
| 切片赋值                | "seq[i:j] = values"       | "setitem(seq, slice(i, j), values)"     |
+-------------------------+---------------------------+-----------------------------------------+
| 切片删除                | "del seq[i:j]"            | "delitem(seq, slice(i, j))"             |
+-------------------------+---------------------------+-----------------------------------------+
| 切片取值                | "seq[i:j]"                | "getitem(seq, slice(i, j))"             |
+-------------------------+---------------------------+-----------------------------------------+
| 字符串格式化            | "s % obj"                 | "mod(s, obj)"                           |
+-------------------------+---------------------------+-----------------------------------------+
| 减法                    | "a - b"                   | "sub(a, b)"                             |
+-------------------------+---------------------------+-----------------------------------------+
| 真值测试                | "obj"                     | "truth(obj)"                            |
+-------------------------+---------------------------+-----------------------------------------+
| 比较                    | "a < b"                   | "lt(a, b)"                              |
+-------------------------+---------------------------+-----------------------------------------+
| 比较                    | "a <= b"                  | "le(a, b)"                              |
+-------------------------+---------------------------+-----------------------------------------+
| 相等                    | "a == b"                  | "eq(a, b)"                              |
+-------------------------+---------------------------+-----------------------------------------+
| 不等                    | "a != b"                  | "ne(a, b)"                              |
+-------------------------+---------------------------+-----------------------------------------+
| 比较                    | "a >= b"                  | "ge(a, b)"                              |
+-------------------------+---------------------------+-----------------------------------------+
| 比较                    | "a > b"                   | "gt(a, b)"                              |
+-------------------------+---------------------------+-----------------------------------------+


原地运算符
==========

许多运算都有“原地”版本。 以下列出的是提供对原地运算符相比通常语法更底
层访问的函数，例如 *statement* "x += y" 相当于 "x = operator.iadd(x,
y)"。 换一种方式来讲就是 "z = operator.iadd(x, y)" 等价于语句块 "z =
x; z += y"。

在这些例子中，请注意当调用一个原地方法时，运算和赋值是分成两个步骤来执
行的。 下面列出的原地函数只执行第一步即调用原地方法。 第二步赋值则不加
处理。

对于不可变的目标例如字符串、数字和元组，更新的值会被计算，但不会被再被
赋值给输入变量：

>>> a = 'hello'
>>> iadd(a, ' world')
'hello world'
>>> a
'hello'

对于可变的目标例如列表和字典，原地方法将执行更新，因此不需要后续赋值操
作：

>>> s = ['h', 'e', 'l', 'l', 'o']
>>> iadd(s, [' ', 'w', 'o', 'r', 'l', 'd'])
['h', 'e', 'l', 'l', 'o', ' ', 'w', 'o', 'r', 'l', 'd']
>>> s
['h', 'e', 'l', 'l', 'o', ' ', 'w', 'o', 'r', 'l', 'd']

operator.iadd(a, b)
operator.__iadd__(a, b)

   "a = iadd(a, b)" 等价于 "a += b"。

operator.iand(a, b)
operator.__iand__(a, b)

   "a = iand(a, b)" 等价于 "a &= b"。

operator.iconcat(a, b)
operator.__iconcat__(a, b)

   "a = iconcat(a, b)" 等价于 "a += b" 其中 *a* 和 *b* 为序列。

operator.ifloordiv(a, b)
operator.__ifloordiv__(a, b)

   "a = ifloordiv(a, b)" 等价于 "a //= b"。

operator.ilshift(a, b)
operator.__ilshift__(a, b)

   "a = ilshift(a, b)" 等价于 "a <<= b"。

operator.imod(a, b)
operator.__imod__(a, b)

   "a = imod(a, b)" 等价于 "a %= b"。

operator.imul(a, b)
operator.__imul__(a, b)

   "a = imul(a, b)" 等价于 "a *= b"。

operator.imatmul(a, b)
operator.__imatmul__(a, b)

   "a = imatmul(a, b)" 等价于 "a @= b"。

   3.5 新版功能.

operator.ior(a, b)
operator.__ior__(a, b)

   "a = ior(a, b)" 等价于 "a |= b"。

operator.ipow(a, b)
operator.__ipow__(a, b)

   "a = ipow(a, b)" 等价于 "a **= b"。

operator.irshift(a, b)
operator.__irshift__(a, b)

   "a = irshift(a, b)" 等价于 "a >>= b"。

operator.isub(a, b)
operator.__isub__(a, b)

   "a = isub(a, b)" 等价于 "a -= b"。

operator.itruediv(a, b)
operator.__itruediv__(a, b)

   "a = itruediv(a, b)" 等价于 "a /= b"。

operator.ixor(a, b)
operator.__ixor__(a, b)

   "a = ixor(a, b)" 等价于 "a ^= b"。
