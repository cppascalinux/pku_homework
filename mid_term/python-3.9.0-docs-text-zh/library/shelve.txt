"shelve" --- Python 对象持久化
******************************

**源代码:** Lib/shelve.py

======================================================================

"Shelf" 是一种持久化的类似字典的对象。 与 "dbm" 数据库的区别在于 Shelf
中的值（不是键！）实际上可以为任意 Python 对象 --- 即 "pickle" 模块能
够处理的任何东西。 这包括大部分类实例、递归数据类型，以及包含大量共享
子对象的对象。 键则为普通的字符串。

shelve.open(filename, flag='c', protocol=None, writeback=False)

   打开一个持久化字典。 filename 指定下层数据库的基准文件名。 作为附带
   效果，会为 filename 添加一个扩展名并且可能创建更多的文件。 默认情况
   下，下层数据库会以读写模式打开。 可选的 *flag* 形参具有与
   "dbm.open()" *flag* 形参相同的含义。

   默认会使用第 3 版 pickle 协议来序列化值。  pickle 协议版本可通过
   *protocol* 形参来指定。

   由于 Python 语义的限制，Shelf 对象无法确定一个可变的持久化字典条目
   在何时被修改。 默认情况下 *只有* 在被修改对象再赋值给 shelf 时才会
   写入该对象 (参见 示例)。 如果可选的 *writeback* 形参设为 "True"，则
   所有被访问的条目都将在内存中被缓存，并会在 "sync()" 和 "close()" 时
   被写入；这可以使得对持久化字典中可变条目的修改更方便，但是如果访问
   的条目很多，这会消耗大量内存作为缓存，并会使得关闭操作变得非常缓慢
   ，因为所有被访问的条目都需要写回到字典（无法确定被访问的条目中哪个
   是可变的，也无法确定哪个被实际修改了）。

   注解:

     请不要依赖于 Shelf 的自动关闭功能；当你不再需要时应当总是显式地调
     用 "close()"，或者使用 "shelve.open()" 作为上下文管理器:

        with shelve.open('spam') as db:
            db['eggs'] = 'eggs'

警告:

  由于 "shelve" 模块需要 "pickle" 的支持，因此从不可靠的来源载入 shelf
  是不安全的。 与 pickle 一样，载入 Shelf 时可以执行任意代码。

字典所支持的所有方法都被 Shelf 对象所支持。 因此很容易将基于字典的代码
转换为需要持久化存储的代码。

额外支持的两个方法：

Shelf.sync()

   如果 Shelf 打开时将 *writeback* 设为 "True" 则写回缓存中的所有条目
   。 如果可行还会清空缓存并将持久化字典同步到磁盘。 此方法会在使用
   "close()" 关闭 Shelf 时自动被调用。

Shelf.close()

   同步并关闭持久化 *dict* 对象。 对已关闭 Shelf 的操作将失败并引发
   "ValueError"。

参见: 持久化字典方案，使用了广泛支持的存储格式并具有原生字典的速度。


限制
====

* 可选择使用哪种数据库包 (例如 "dbm.ndbm" 或 "dbm.gnu") 取决于支持哪种
  接口。 因此使用 "dbm" 直接打开数据库是不安全的。 如果使用了 "dbm"，
  数据库同样会（不幸地）受限于它 --- 这意味着存储在数据库中的（封存形
  式的）对象尺寸应当较小，并且在少数情况下键冲突有可能导致数据库拒绝更
  新。

* "shelve" 模块不支持对 Shelf 对象的 *并发* 读/写访问。 （多个同时读取
  访问则是安全的。） 当一个程序打开一个 shelve 对象来写入时，不应再有
  其他程序同时打开它来读取或写入。 Unix 文件锁定可被用来解决此问题，但
  这在不同 Unix 版本上会存在差异，并且需要有关所用数据库实现的细节知识
  。

class shelve.Shelf(dict, protocol=None, writeback=False, keyencoding='utf-8')

   "collections.abc.MutableMapping" 的一个子类，它会将封存的值保存在
   *dict* 对象中。

   默认会使用第 3 版 pickle 协议来序列化值。 pickle 协议版本可通过
   *protocol* 形参来指定。 请参阅 "pickle" 文档来查看 pickle 协议的相
   关讨论。

   如果 *writeback* 形参为 "True"，对象将为所有访问过的条目保留缓存并
   在同步和关闭时将它们写回到 *dict*。 这允许对可变的条目执行自然操作
   ，但是会消耗更多内存并让同步和关闭花费更长时间。

   *keyencoding* 形参是在下层字典被使用之前用于编码键的编码格式。

   "Shelf" 对象还可以被用作上下文管理器，在这种情况下它将在 "with" 语
   句块结束时自动被关闭。

   在 3.2 版更改: 添加了 *keyencoding* 形参；之前，键总是使用 UTF-8 编
   码。

   在 3.4 版更改: 添加了上下文管理器支持

class shelve.BsdDbShelf(dict, protocol=None, writeback=False, keyencoding='utf-8')

   "Shelf" 的一个子类，将 "first()", "next()", "previous()", "last()"
   和 "set_location()" 对外公开，在来自 pybsddb 的第三方 "bsddb" 模块
   中可用，但在其他数据库模块中不可用。 传给构造器的 *dict* 对象必须支
   持这些方法。 这通常是通过调用 "bsddb.hashopen()", "bsddb.btopen()"
   或 "bsddb.rnopen()" 之一来完成的。  可选的 *protocol*, *writeback*
   和 *keyencoding* 形参具有与 "Shelf" 类相同的含义。

class shelve.DbfilenameShelf(filename, flag='c', protocol=None, writeback=False)

   "Shelf" 的一个子类，它接受一个 *filename* 而非字典类对象。 下层文件
   将使用 "dbm.open()" 来打开。 默认情况下，文件将以读写模式打开。 可
   选的 *flag* 形参具有与 "open()" 函数相同的含义。 可选的 *protocol*
   和 *writeback* 形参具有与 "Shelf" 类相同的含义。


示例
====

对接口的总结如下 ("key" 为字符串，"data" 为任意对象):

   import shelve

   d = shelve.open(filename)  # open -- file may get suffix added by low-level
                              # library

   d[key] = data              # store data at key (overwrites old data if
                              # using an existing key)
   data = d[key]              # retrieve a COPY of data at key (raise KeyError
                              # if no such key)
   del d[key]                 # delete data stored at key (raises KeyError
                              # if no such key)

   flag = key in d            # true if the key exists
   klist = list(d.keys())     # a list of all existing keys (slow!)

   # as d was opened WITHOUT writeback=True, beware:
   d['xx'] = [0, 1, 2]        # this works as expected, but...
   d['xx'].append(3)          # *this doesn't!* -- d['xx'] is STILL [0, 1, 2]!

   # having opened d without writeback=True, you need to code carefully:
   temp = d['xx']             # extracts the copy
   temp.append(5)             # mutates the copy
   d['xx'] = temp             # stores the copy right back, to persist it

   # or, d=shelve.open(filename,writeback=True) would let you just code
   # d['xx'].append(5) and have it work as expected, BUT it would also
   # consume more memory and make the d.close() operation slower.

   d.close()                  # close it

参见:

  模块 "dbm"
     "dbm" 风格数据库的泛型接口。

  模块 "pickle"
     "shelve" 所使用的对象序列化。
