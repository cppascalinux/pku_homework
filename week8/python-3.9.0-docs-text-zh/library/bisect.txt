"bisect" --- 数组二分查找算法
*****************************

**源代码：** Lib/bisect.py

======================================================================

这个模块对有序列表提供了支持，使得他们可以在插入新数据仍然保持有序。对
于长列表，如果其包含元素的比较操作十分昂贵的话，这可以是对更常见方法的
改进。这个模块叫做 "bisect" 因为其使用了基本的二分（bisection）算法。
源代码也可以作为很棒的算法示例（边界判断也做好啦！）

定义了以下函数：

bisect.bisect_left(a, x, lo=0, hi=len(a))

   在 *a* 中找到 *x* 合适的插入点以维持有序。参数 *lo* 和 *hi* 可以被
   用于确定需要考虑的子集；默认情况下整个列表都会被使用。如果 *x* 已经
   在 *a* 里存在，那么插入点会在已存在元素之前（也就是左边）。如果 *a*
   是列表（list）的话，返回值是可以被放在 "list.insert()" 的第一个参数
   的。

   返回的插入点 *i* 可以将数组 *a* 分成两部分。左侧是 "all(val < x for
   val in a[lo:i])" ，右侧是 "all(val >= x for val in a[i:hi])" 。

bisect.bisect_right(a, x, lo=0, hi=len(a))
bisect.bisect(a, x, lo=0, hi=len(a))

   类似于 "bisect_left()"，但是返回的插入点是 *a* 中已存在元素 *x* 的
   右侧。

   返回的插入点 *i* 可以将数组 *a* 分成两部分。左侧是 "all(val <= x
   for val in a[lo:i])"，右侧是 "all(val > x for val in a[i:hi])" for
   the right side。

bisect.insort_left(a, x, lo=0, hi=len(a))

   将 *x* 插入到一个有序序列 *a* 里，并维持其有序。如果 *a* 有序的话，
   这相当于 "a.insert(bisect.bisect_left(a, x, lo, hi), x)"。要注意搜
   索是 O(log n) 的，插入却是 O(n) 的。

bisect.insort_right(a, x, lo=0, hi=len(a))
bisect.insort(a, x, lo=0, hi=len(a))

   类似于 "insort_left()"，但是把 *x* 插入到 *a* 中已存在元素 *x* 的右
   侧。

参见:

  SortedCollection recipe 使用 bisect 构造了一个功能完整的集合类，提供
  了直接的搜索方法和对用于搜索的 key 方法的支持。所有用于搜索的键都是
  预先计算的，以避免在搜索时对 key 方法的不必要调用。


搜索有序列表
============

上面的 "bisect()" 函数对于找到插入点是有用的，但在一般的搜索任务中可能
会有点尴尬。下面 5 个函数展示了如何将其转变成有序列表中的标准查找函数

   def index(a, x):
       'Locate the leftmost value exactly equal to x'
       i = bisect_left(a, x)
       if i != len(a) and a[i] == x:
           return i
       raise ValueError

   def find_lt(a, x):
       'Find rightmost value less than x'
       i = bisect_left(a, x)
       if i:
           return a[i-1]
       raise ValueError

   def find_le(a, x):
       'Find rightmost value less than or equal to x'
       i = bisect_right(a, x)
       if i:
           return a[i-1]
       raise ValueError

   def find_gt(a, x):
       'Find leftmost value greater than x'
       i = bisect_right(a, x)
       if i != len(a):
           return a[i]
       raise ValueError

   def find_ge(a, x):
       'Find leftmost item greater than or equal to x'
       i = bisect_left(a, x)
       if i != len(a):
           return a[i]
       raise ValueError


其他示例
========

函数 "bisect()" 还可以用于数字表查询。这个例子是使用 "bisect()" 从一个
给定的考试成绩集合里，通过一个有序数字表，查出其对应的字母等级：90 分
及以上是 'A'，80 到 89 是 'B'，以此类推

   >>> def grade(score, breakpoints=[60, 70, 80, 90], grades='FDCBA'):
   ...     i = bisect(breakpoints, score)
   ...     return grades[i]
   ...
   >>> [grade(score) for score in [33, 99, 77, 70, 89, 90, 100]]
   ['F', 'A', 'C', 'C', 'B', 'A', 'A']

与 "sorted()" 函数不同，对于 "bisect()" 函数来说，*key* 或者
*reversed* 参数并没有什么意义。因为这会导致设计效率低下（连续调用
bisect 函数时，是不会 "记住" 过去查找过的键的）。

正相反，最好去搜索预先计算好的键列表，来查找相关记录的索引。

   >>> data = [('red', 5), ('blue', 1), ('yellow', 8), ('black', 0)]
   >>> data.sort(key=lambda r: r[1])
   >>> keys = [r[1] for r in data]         # precomputed list of keys
   >>> data[bisect_left(keys, 0)]
   ('black', 0)
   >>> data[bisect_left(keys, 1)]
   ('blue', 1)
   >>> data[bisect_left(keys, 5)]
   ('red', 5)
   >>> data[bisect_left(keys, 8)]
   ('yellow', 8)
