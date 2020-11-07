"xdrlib" --- 编码与解码 XDR 数据
********************************

**源代码:** Lib/xdrlib.py

======================================================================

"xdrlib" 模块为外部数据表示标准提供支持，该标准的描述见 **RFC 1014**，
由 Sun Microsystems, Inc. 在 1987 年 6 月撰写。 它支持该 RFC 中描述的
大部分数据类型。

"xdrlib" 模块定义了两个类，一个用于将变量打包为 XDR 表示形式，另一个用
于从 XDR 表示形式解包。 此外还有两个异常类。

class xdrlib.Packer

   "Packer" 是用于将数据打包为 XDR 表示形式的类。 "Packer" 类的实例化
   不附带参数。

class xdrlib.Unpacker(data)

   "Unpacker" 是用于相应地从字符串缓冲区解包 XDR 数据值的类。 输入缓冲
   区将作为 *data* 给出。

参见:

  **RFC 1014** - XDR: 外部数据表示标准
     这个 RFC 定义了最初编写此模块时 XDR 所用的数据编码格式。 显然它已
     被 **RFC 1832** 所淘汰。

  **RFC 1832** - XDR: 外部数据表示标准
     更新的 RFC，它提供了经修订的 XDR 定义。


Packer 对象
===========

"Packer" 实例具有下列方法:

Packer.get_buffer()

   将当前打包缓冲区以字符串的形式返回。

Packer.reset()

   将打包缓冲区重置为空字符串。

总体来说，你可以通过调用适当的 "pack_type()" 方法来打包任何最常见的
XDR 数据类型。 每个方法都是接受单个参数，即要打包的值。 受支持的简单数
据类型打包方法如下: "pack_uint()", "pack_int()", "pack_enum()",
"pack_bool()", "pack_uhyper()" 以及 "pack_hyper()"。

Packer.pack_float(value)

   打包单精度浮点数 *value*。

Packer.pack_double(value)

   打包双精度浮点数 *value*。

以下方法支持打包字符串、字节串以及不透明数据。

Packer.pack_fstring(n, s)

   打包固定长度字符串 *s*。 *n* 为字符串的长度，但它 *不会* 被打包进数
   据缓冲区。 如有必要字符串会以空字节串填充以保证 4 字节对齐。

Packer.pack_fopaque(n, data)

   打包固定长度不透明数据流，类似于 "pack_fstring()"。

Packer.pack_string(s)

   打包可变长度字符串 *s*。 先将字符串的长度打包为无符号整数，再用
   "pack_fstring()" 来打包字符串数据。

Packer.pack_opaque(data)

   打包可变长度不透明数据流，类似于 "pack_string()"。

Packer.pack_bytes(bytes)

   打包可变长度字节流，类似于 "pack_string()"。

下列方法支持打包数组和列表:

Packer.pack_list(list, pack_item)

   打包由同质条目构成的 *list*。 此方法适用于不确定长度的列表；即其长
   度无法在遍历整个列表之前获知。 对于列表中的每个条目，先打包一个无符
   号整数 "1"，再添加列表中数据的值。 *pack_item* 是在打包单个条目时要
   调用的函数。 在列表的末尾，会再打包一个无符号整数 "0"。

   例如，要打包一个整数列表，代码看起来会是这样:

      import xdrlib
      p = xdrlib.Packer()
      p.pack_list([1, 2, 3], p.pack_int)

Packer.pack_farray(n, array, pack_item)

   打包由同质条目构成的固定长度列表 (*array*)。 *n* 为列表长度；它 *不
   会* 被打包到缓冲区，但是如果 "len(array)" 不等于 *n* 则会引发
   "ValueError"。 如上所述，*pack_item* 是在打包每个元素时要使用的函数
   。

Packer.pack_array(list, pack_item)

   打包由同质条目构成的可变长度 *list*。 先将列表的长度打包为无符号整
   数，再像上面的 "pack_farray()" 一样打包每个元素。


Unpacker 对象
=============

"Unpacker" 类提供以下方法:

Unpacker.reset(data)

   使用给定的 *data* 重置字符串缓冲区。

Unpacker.get_position()

   返回数据缓冲区中的当前解包位置。

Unpacker.set_position(position)

   将数据缓冲区的解包位置设为 *position*。 你应当小心使用
   "get_position()" 和 "set_position()"。

Unpacker.get_buffer()

   将当前解包数据缓冲区以字符串的形式返回。

Unpacker.done()

   表明解包完成。 如果数据没有全部完成解包则会引发 "Error" 异常。

此外，每种可通过 "Packer" 打包的数据类型都可通过 "Unpacker" 来解包。
解包方法的形式为 "unpack_type()"，并且不接受任何参数。 该方法将返回解
包后的对象。

Unpacker.unpack_float()

   解包单精度浮点数。

Unpacker.unpack_double()

   解包双精度浮点数，类似于 "unpack_float()"。

此外，以下方法可用来解包字符串、字节串以及不透明数据:

Unpacker.unpack_fstring(n)

   解包并返回固定长度字符串。 *n* 为期望的字符数量。 会预设以空字节串
   填充以保证 4 字节对齐。

Unpacker.unpack_fopaque(n)

   解包并返回固定长度数据流，类似于 "unpack_fstring()"。

Unpacker.unpack_string()

   解包并返回可变长度字符串。 先将字符串的长度解包为无符号整数，再用
   "unpack_fstring()" 来解包字符串数据。

Unpacker.unpack_opaque()

   解包并返回可变长度不透明数据流，类似于 "unpack_string()"。

Unpacker.unpack_bytes()

   解包并返回可变长度字节流，类似于 "unpack_string()"。

下列方法支持解包数组和列表:

Unpacker.unpack_list(unpack_item)

   解包并返回同质条目的列表。 该列表每次解包一个元素，先解包一个无符号
   整数旗标。 如果旗标为 "1"，则解包条目并将其添加到列表。 旗标为 "0"
   表明列表结束。 *unpack_item* 为在解包条目时调用的函数。

Unpacker.unpack_farray(n, unpack_item)

   解包并（以列表形式）返回由同质条目构成的固定长度数组。 *n* 为期望的
   缓冲区内列表元素数量。 如上所述，*unpack_item* 是解包每个元素时要使
   用的函数。

Unpacker.unpack_array(unpack_item)

   解包并返回由同质条目构成的可变长度 *list*。 先将列表的长度解包为无
   符号整数，再像上面的 "unpack_farray()" 一样解包每个元素。


异常
====

此模块中的异常会表示为类实例代码:

exception xdrlib.Error

   基本异常类。 "Error" 具有一个公共属性 "msg"，其中包含对错误的描述。

exception xdrlib.ConversionError

   从 "Error" 所派生的类。 不包含额外的实例变量。

以下是一个应该如何捕获这些异常的示例:

   import xdrlib
   p = xdrlib.Packer()
   try:
       p.pack_double(8.01)
   except xdrlib.ConversionError as instance:
       print('packing the double failed:', instance.msg)
