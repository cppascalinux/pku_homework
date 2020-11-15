"numbers" --- 数字的抽象基类
****************************

**源代码：** Lib/numbers.py

======================================================================

"numbers" 模块 (**PEP 3141**) 定义了数字 *抽象基类* 的层次结构，其中逐
级定义了更多操作。 此模块中所定义的类型都不可被实例化。

class numbers.Number

   数字的层次结构的基础。如果你只想确认参数 *x* 是不是数字而不关心其类
   型，则使用``isinstance(x, Number)``。


数字的层次
==========

class numbers.Complex

   内置在类型 "complex" 里的子类描述了复数和它的运算操作。这些操作有：
   转化至  "complex" 和 "bool"， "real"、 "imag"、"+"、"-"、"*"、"/"、
   "abs()"、 "conjugate()"、 "==" 和 "!="。 所有的异常，"-" 和 "!=" ，
   都是抽象的。

   real

      抽象的。得到该数字的实数部分。

   imag

      抽象的。得到该数字的虚数部分。

   abstractmethod conjugate()

      抽象的。返回共轭复数。例如 "(1+3j).conjugate() == (1-3j)"。

class numbers.Real

   相对于 "Complex"，"Real" 加入了只有实数才能进行的操作。

   简单的说，它们是：转化至 "float"，"math.trunc()"、 "round()"、
   "math.floor()"、 "math.ceil()"、 "divmod()"、 "//"、 "%"、 "<"、
   "<="、 ">"、 和 ">="。

   实数同样默认支持 "complex()"、 "real"、 "imag" 和 "conjugate()"。

class numbers.Rational

   子类型 "Real" 并加入 "numerator" 和 "denominator" 两种属性，这两种
   属性应该属于最低的级别。加入后，这默认支持 "float()"。

   numerator

      摘要。

   denominator

      摘要。

class numbers.Integral

   子类型 "Rational" 加上转化至 "int"。 默认支持 "float()"、
   "numerator" 和 "denominator"。 在 "**" 中加入抽象方法和比特字符串的
   操作： "<<"、 ">>"、 "&"、 "^"、 "|"、 "~"。


类型接口注释。
==============

实现者需要注意使相等的数字相等并拥有同样的值。当这两个数使用不同的扩展
模块时，这其中的差异是很微妙的。例如，用 "fractions.Fraction" 实现
"hash()" 如下:

   def __hash__(self):
       if self.denominator == 1:
           # Get integers right.
           return hash(self.numerator)
       # Expensive check, but definitely correct.
       if self == float(self):
           return hash(float(self))
       else:
           # Use tuple's hash to avoid a high collision rate on
           # simple fractions.
           return hash((self.numerator, self.denominator))


加入更多数字的ABC
-----------------

当然，这里有更多支持数字的ABC，如果不加入这些，就将缺少层次感。你可以
用如下方法在 "Complex" 和 "Real" 中加入``MyFoo``：

   class MyFoo(Complex): ...
   MyFoo.register(Real)


实现算数运算
------------

我们希望实现计算，因此，混合模式操作要么调用一个作者知道参数类型的实现
，要么转变成为最接近的内置类型并对这个执行操作。对于子类 "Integral"，
这意味着 "__add__()" 和 "__radd__()" 必须用如下方式定义：

   class MyIntegral(Integral):

       def __add__(self, other):
           if isinstance(other, MyIntegral):
               return do_my_adding_stuff(self, other)
           elif isinstance(other, OtherTypeIKnowAbout):
               return do_my_other_adding_stuff(self, other)
           else:
               return NotImplemented

       def __radd__(self, other):
           if isinstance(other, MyIntegral):
               return do_my_adding_stuff(other, self)
           elif isinstance(other, OtherTypeIKnowAbout):
               return do_my_other_adding_stuff(other, self)
           elif isinstance(other, Integral):
               return int(other) + int(self)
           elif isinstance(other, Real):
               return float(other) + float(self)
           elif isinstance(other, Complex):
               return complex(other) + complex(self)
           else:
               return NotImplemented

There are 5 different cases for a mixed-type operation on subclasses
of "Complex". I'll refer to all of the above code that doesn't refer
to "MyIntegral" and "OtherTypeIKnowAbout" as "boilerplate". "a" will
be an instance of "A", which is a subtype of "Complex" ("a : A <:
Complex"), and "b : B <: Complex". I'll consider "a + b":

   1. 如果 "A" 被定义成一个承认``b`` 的 "__add__()"，一切都没有问题。

   2. 如果 "A" 转回成“模板”失败，它将返回一个属于 "__add__()" 的值，我
      们需要避免 "B" 定义了一个更加智能的 "__radd__()"，因此模板需要返
      回一个属于 "__add__()" 的 "NotImplemented" 。（或者 "A" 可能完全
      不实现 "__add__()" 。）

   3. 接着看 "B" 的 "__radd__()" 。如果它承认 "a" ，一切都没有问题。

   4. 如果没有成功回退到模板，就没有更多的方法可以去尝试，因此这里将使
      用默认的实现。

   5. 如果 "B <: A" ， Python 在 "A.__add__" 之前尝试 "B.__radd__" 。
      这是可行的，是通过对 "A" 的认识实现的，因此这可以在交给
      "Complex" 处理之前处理这些实例。

如果 "A <: Complex" 和 "B <: Real" 没有共享任何资源，那么适当的共享操
作涉及内置的 "complex" ，并且分别获得 "__radd__()" ，因此 "a+b == b+a"
。

由于对任何一直类型的大部分操作是十分相似的，可以定义一个帮助函数，即一
个生成后续或相反的实例的生成器。例如，使用 "fractions.Fraction" 如下：

   def _operator_fallbacks(monomorphic_operator, fallback_operator):
       def forward(a, b):
           if isinstance(b, (int, Fraction)):
               return monomorphic_operator(a, b)
           elif isinstance(b, float):
               return fallback_operator(float(a), b)
           elif isinstance(b, complex):
               return fallback_operator(complex(a), b)
           else:
               return NotImplemented
       forward.__name__ = '__' + fallback_operator.__name__ + '__'
       forward.__doc__ = monomorphic_operator.__doc__

       def reverse(b, a):
           if isinstance(a, Rational):
               # Includes ints.
               return monomorphic_operator(a, b)
           elif isinstance(a, numbers.Real):
               return fallback_operator(float(a), float(b))
           elif isinstance(a, numbers.Complex):
               return fallback_operator(complex(a), complex(b))
           else:
               return NotImplemented
       reverse.__name__ = '__r' + fallback_operator.__name__ + '__'
       reverse.__doc__ = monomorphic_operator.__doc__

       return forward, reverse

   def _add(a, b):
       """a + b"""
       return Fraction(a.numerator * b.denominator +
                       b.numerator * a.denominator,
                       a.denominator * b.denominator)

   __add__, __radd__ = _operator_fallbacks(_add, operator.add)

   # ...
