"sndhdr" --- 推测声音文件的类型
*******************************

**源代码** Lib/sndhdr.py

======================================================================

"sndhdr" 提供了企图猜测文件中的声音数据类型的功能函数。当这些函数可以
推测出存储在文件中的声音数据的类型是，它们返回一个
"collections.namedtuple()"，包含了五种属性：（"filetype", "framerate",
"nchannels", "nframes", "sampwidth"）。这些 *type* 的值表示数据的类型
，会是以下字符串之一： "'aifc'", "'aiff'", "'au'", "'hcom'", "'sndr'",
"'sndt'", "'voc'", "'wav'", "'8svx'", "'sb'", "'ub'", or "'ul'" 。
*sampling_rate* 可能是实际值或者当未知或者难以解码时的 "0"。类似的，
*channels* 也会返回实际值或者在无法推测或者难以解码时返回 "0"。
*frames* 则是实际值或 "-1"。 元组的最后一项， *bits_per_sample* 将会为
比特表示的 sample 大小或者 A-LAW 时为 "'A'"， u-LAW 时为 "'U'"。

sndhdr.what(filename)

   使用 "whathdr()" 推测存储在 *filename* 文件中的声音数据的类型。如果
   成功，返回上述的命名元组，否则返回 "None"。

   在 3.5 版更改: 将结果从元组改为命名元组。

sndhdr.whathdr(filename)

   基于文件头推测存储在文件中的声音数据类型。文件名由 *filename* 给出
   。这个函数在成功时返回上述命名元组，或者在失败时返回 "None"。

   在 3.5 版更改: 将结果从元组改为命名元组。
