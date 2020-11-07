DateTime 对象
*************

"datetime" 模块提供了各种日期和时间对象。 在使用任何这些函数之前，必须
在你的源码中包含头文件 "datetime.h" (请注意此文件并未包含在 "Python.h"
中)，并且宏 "PyDateTime_IMPORT" 必须被发起调用，通常是作为模块初始化函
数的一部分。 这个宏会将指向特定 C 结构的指针放入一个静态变量
"PyDateTimeAPI" 中，它会由下面的宏来使用。

宏访问UTC单例:

PyObject* PyDateTime_TimeZone_UTC

   返回表示 UTC 的时区单例，与 "datetime.timezone.utc" 为同一对象。

   3.7 新版功能.

类型检查宏：

int PyDate_Check(PyObject *ob)

   如果 *ob* 为 "PyDateTime_DateType" 类型或 "PyDateTime_DateType" 的
   某个子类型则返回真值。 *ob* 不能为 "NULL"。

int PyDate_CheckExact(PyObject *ob)

   如果 *ob* 为 "PyDateTime_DateType" 类型则返回真值。 *ob* 不能为
   "NULL"。

int PyDateTime_Check(PyObject *ob)

   如果 *ob* 为 "PyDateTime_DateTimeType" 类型或
   "PyDateTime_DateTimeType" 的某个子类型则返回真值。 *ob* 不能为
   "NULL"。

int PyDateTime_CheckExact(PyObject *ob)

   如果 *ob* 为 "PyDateTime_DateTimeType" 类型则返回真值。 *ob* 不能为
   "NULL"。

int PyTime_Check(PyObject *ob)

   如果 *ob* 的类型是 "PyDateTime_TimeType" 或是 "PyDateTime_TimeType"
   的子类型则返回真值。 *ob* 必须不为 "NULL"。

int PyTime_CheckExact(PyObject *ob)

   如果 *ob* 的类型是 "PyDateTime_TimeType" 则返回真值。 *ob* 必须不为
   "NULL"。

int PyDelta_Check(PyObject *ob)

   如果 *ob* 为 "PyDateTime_DeltaType" 类型或 "PyDateTime_DeltaType"
   的某个子类型则返回真值。 *ob* 不能为 "NULL"。

int PyDelta_CheckExact(PyObject *ob)

   如果 *ob* 为 "PyDateTime_DeltaType" 类型则返回真值。 *ob* 不能为
   "NULL"。

int PyTZInfo_Check(PyObject *ob)

   如果 *ob* 为 "PyDateTime_TZInfoType" 类型或 "PyDateTime_TZInfoType"
   的某个子类型则返回真值。 *ob* 不能为  "NULL"。

int PyTZInfo_CheckExact(PyObject *ob)

   如果 *ob* 的类型是 "PyDateTime_TZInfoType" 则返回真值。 *ob* 不能为
   "NULL"。

用于创建对象的宏：

PyObject* PyDate_FromDate(int year, int month, int day)
    *Return value: New reference.*

   返回指定年、月、日的 "datetime.date" 对象。

PyObject* PyDateTime_FromDateAndTime(int year, int month, int day, int hour, int minute, int second, int usecond)
    *Return value: New reference.*

   返回具有指定 year, month, day, hour, minute, second 和 microsecond
   属性的 "datetime.datetime" 对象。

PyObject* PyDateTime_FromDateAndTimeAndFold(int year, int month, int day, int hour, int minute, int second, int usecond, int fold)
    *Return value: New reference.*

   返回具有指定 year, month, day, hour, minute, second, microsecond 和
   fold 属性的 "datetime.datetime" 对象。

   3.6 新版功能.

PyObject* PyTime_FromTime(int hour, int minute, int second, int usecond)
    *Return value: New reference.*

   返回具有指定 hour, minute, second and microsecond 属性的
   "datetime.time" 对象。

PyObject* PyTime_FromTimeAndFold(int hour, int minute, int second, int usecond, int fold)
    *Return value: New reference.*

   返回具有指定 hour, minute, second, microsecond 和 fold 属性的
   "datetime.time" 对象。

   3.6 新版功能.

PyObject* PyDelta_FromDSU(int days, int seconds, int useconds)
    *Return value: New reference.*

   返回代表给定天、秒和微秒数的 "datetime.timedelta" 对象。 将执行正规
   化操作以使最终的微秒和秒数处在 "datetime.timedelta" 对象的文档指明
   的区间之内。

PyObject* PyTimeZone_FromOffset(PyDateTime_DeltaType* offset)
    *Return value: New reference.*

   返回一个 "datetime.timezone" 对象，该对象具有以 *offset* 参数表示
   的未命名固定时差。

   3.7 新版功能.

PyObject* PyTimeZone_FromOffsetAndName(PyDateTime_DeltaType* offset, PyUnicode* name)
    *Return value: New reference.*

   返回一个 "datetime.timezone" 对象，该对象具有以 *offset* 参数表示的
   固定时差和时区名称 *name*。

   3.7 新版功能.

一些用来从 date 对象中提取字段的宏。 参数必须是 "PyDateTime_Date" 包括
其子类 (例如 "PyDateTime_DateTime") 的实例。 参数必须不为 "NULL"，并且
类型不被会检查:

int PyDateTime_GET_YEAR(PyDateTime_Date *o)

   以正整数的形式返回年份值。

int PyDateTime_GET_MONTH(PyDateTime_Date *o)

   返回月，从0到12的整数。

int PyDateTime_GET_DAY(PyDateTime_Date *o)

   返回日期，从0到31的整数。

一些用来从 datetime 对象中提取字段的宏。 参数必须是
"PyDateTime_DateTime" 包括其子类的实例。 参数必须不为 "NULL"，并且类型
不会被检查:

int PyDateTime_DATE_GET_HOUR(PyDateTime_DateTime *o)

   返回小时，从0到23的整数。

int PyDateTime_DATE_GET_MINUTE(PyDateTime_DateTime *o)

   返回分钟，从0到59的整数。

int PyDateTime_DATE_GET_SECOND(PyDateTime_DateTime *o)

   返回秒，从0到59的整数。

int PyDateTime_DATE_GET_MICROSECOND(PyDateTime_DateTime *o)

   返回微秒，从0到999999的整数。

一些用来从 time 对象中提取字段的宏。 参数必须是 "PyDateTime_Time" 包括
其子类的实例。 参数必须不为 "NULL"，并且类型不会被检查:

int PyDateTime_TIME_GET_HOUR(PyDateTime_Time *o)

   返回小时，从0到23的整数。

int PyDateTime_TIME_GET_MINUTE(PyDateTime_Time *o)

   返回分钟，从0到59的整数。

int PyDateTime_TIME_GET_SECOND(PyDateTime_Time *o)

   返回秒，从0到59的整数。

int PyDateTime_TIME_GET_MICROSECOND(PyDateTime_Time *o)

   返回微秒，从0到999999的整数。

一些用来从 timedelta 对象中提取字段的宏。 参数必须是
"PyDateTime_Delta" 包括其子类的实例。 参数必须不为 "NULL"，并且类型不
会被检查:

int PyDateTime_DELTA_GET_DAYS(PyDateTime_Delta *o)

   返回天数，从-999999999到999999999的整数。

   3.3 新版功能.

int PyDateTime_DELTA_GET_SECONDS(PyDateTime_Delta *o)

   返回秒数，从0到86399的整数。

   3.3 新版功能.

int PyDateTime_DELTA_GET_MICROSECONDS(PyDateTime_Delta *o)

   返回微秒数，从0到999999的整数。

   3.3 新版功能.

一些便于模块实现 DB API 的宏:

PyObject* PyDateTime_FromTimestamp(PyObject *args)
    *Return value: New reference.*

   创建并返回一个给定元组参数的新 "datetime.datetime" 对象，适合传给
   "datetime.datetime.fromtimestamp()"。

PyObject* PyDate_FromTimestamp(PyObject *args)
    *Return value: New reference.*

   创建并返回一个给定元组参数的新 "datetime.date" 对象，适合传给
   "datetime.date.fromtimestamp()"。
