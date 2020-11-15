"lzma" --- 用 LZMA 算法压缩
***************************

3.3 新版功能.

**源代码：** Lib/lzma.py

======================================================================

此模块提供了可以压缩和解压缩使用 LZMA 压缩算法的数据的类和便携函数。
其中还包含支持 **xz** 工具所使用的 ".xz" 和旧式 ".lzma" 文件格式的文件
接口，以及相应的原始压缩数据流。

此模块所提供的接口与 "bz2" 模块的非常类似。 但是，请注意 "LZMAFile" *
不是* 线程安全的，这与 "bz2.BZ2File" 不同，因此如果你需要在多个线程中
使用单个 "LZMAFile" 实例，则需要通过锁来保护它。

exception lzma.LZMAError

   当在压缩或解压缩期间或是在初始化压缩器/解压缩器的状态期间发生错误时
   此异常会被引发。


读写压缩文件
============

lzma.open(filename, mode="rb", *, format=None, check=-1, preset=None, filters=None, encoding=None, errors=None, newline=None)

   以二进制或文本模式打开 LZMA 压缩文件，返回一个 *file object*。

   *filename* 参数可以是一个实际的文件名（以 "str", "bytes" 或 *路径类
   * 对象的形式给出），在此情况下会打开指定名称的文件，或者可以是一个
   用于读写的现有文件对象。

   *mode* 参数可以是二进制模式的 ""r"", ""rb"", ""w"", ""wb"", ""x"",
   ""xb"", ""a"" 或 ""ab""，或者文本模式的 ""rt"", ""wt"", ""xt"" 或
   ""at""。 默认值为 ""rb""。

   当打开一个文件用于读取时，*format* 和 *filters* 参数具有与
   "LZMADecompressor" 的参数相同的含义。 在此情况下，*check* 和
   *preset* 参数不应被使用。

   当打开一个文件用于写入的，*format*, *check*, *preset* 和 *filters*
   参数具有与 "LZMACompressor" 的参数相同的含义。

   对于二进制模式，这个函数等价于 "LZMAFile" 构造器:
   "LZMAFile(filename, mode, ...)"。 在这种情况下，不可提供
   *encoding*, *errors* 和 *newline* 参数。

   对于文本模式，将会创建一个 "LZMAFile" 对象，并将它包装到一个
   "io.TextIOWrapper" 实例中，此实例带有指定的编码格式、错误处理行为和
   行结束符。

   在 3.4 版更改: 增加了对 ""x"", ""xb"" 和 ""xt"" 模式的支持。

   在 3.6 版更改: 接受一个 *类路径对象*。

class lzma.LZMAFile(filename=None, mode="r", *, format=None, check=-1, preset=None, filters=None)

   以二进制模式打开一个 LZMA 压缩文件。

   "LZMAFile" 可以包装在一个已打开的 *file object* 中，或者是在给定名
   称的文件上直接操作。 *filename* 参数指定所包装的文件对象，或是要打
   开的文件名称（类型为 "str", "bytes" 或 *路径类* 对象）。 如果是包装
   现有的文件对象，被包装的文件在 "LZMAFile" 被关闭时将不会被关闭。

   *mode* 参数可以是表示读取的 ""r"" (默认值)，表示覆写的 ""w""，表示
   单独创建的 ""x""，或表示添加的 ""a""。 这些模式还可以分别以 ""rb"",
   ""wb"", ""xb"" 和 ""ab"" 的等价形式给出。

   如果 *filename* 是一个文件对象（而不是实际的文件名），则 ""w"" 模式
   并不会截断文件，而会等价于 ""a""。

   当打开一个文件用于读取时，输入文件可以为多个独立压缩流的拼接。 它们
   会被作为单个逻辑流被透明地解码。

   当打开一个文件用于读取时，*format* 和 *filters* 参数具有与
   "LZMADecompressor" 的参数相同的含义。 在此情况下，*check* 和
   *preset* 参数不应被使用。

   当打开一个文件用于写入的，*format*, *check*, *preset* 和 *filters*
   参数具有与 "LZMACompressor" 的参数相同的含义。

   "LZMAFile" 支持 "io.BufferedIOBase" 所指定的所有成员，但 "detach()"
   和 "truncate()" 除外。 并支持迭代和 "with" 语句。

   也提供以下方法：

   peek(size=-1)

      返回缓冲的数据而不前移文件位置。 至少将返回一个字节的数据，除非
      已经到达 EOF。 实际返回的字节数不确定（会忽略 *size* 参数）。

      注解:

        虽然调用 "peek()" 不会改变 "LZMAFile" 的文件位置，但它可能改变
        下层文件对象的位置（举例来说如果 "LZMAFile" 是通过传入一个文件
        对象作为 *filename* 的话）。

   在 3.4 版更改: 增加了对 ""x"" 和 ""xb"" 模式的支持。

   在 3.5 版更改: "read()" 方法现在接受 "None" 作为参数。

   在 3.6 版更改: 接受一个 *类路径对象*。


在内存中压缩和解压缩数据
========================

class lzma.LZMACompressor(format=FORMAT_XZ, check=-1, preset=None, filters=None)

   创建一个压缩器对象，此对象可被用来执行增量压缩。

   压缩单个数据块的更便捷方式请参阅 "compress()"。

   *format* 参数指定应当使用哪种容器格式。 可能的值有：

   * "FORMAT_XZ": ".xz" 容器格式。
        这是默认格式。

   * "FORMAT_ALONE": 传统的 ".lzma" 容器格式。
        这种格式相比 ".xz" 更为受限 -- 它不支持一致性检查或多重过滤器
        。

   * "FORMAT_RAW": 原始数据流，不使用任何容器格式。
        这个格式描述器不支持一致性检查，并且要求你必须指定一个自定义的
        过滤器链（用于压缩和解压缩）。 此外，以这种方式压缩的数据不可
        使用 "FORMAT_AUTO" 来解压缩 (参见 "LZMADecompressor")。

   *check* 参数指定要包含在压缩数据中的一致性检查类型。 这种检查在解压
   缩时使用，以确保数据没有被破坏。 可能的值是：

   * "CHECK_NONE": 没有一致性检查。 这是 "FORMAT_ALONE" 和
     "FORMAT_RAW" 的默认值（也是唯一可接受的值）。

   * "CHECK_CRC32": 32 位循环冗余检查。

   * "CHECK_CRC64": 64 位循环冗余检查。 这是 "FORMAT_XZ" 的默认值。

   * "CHECK_SHA256": 256 位安全哈希算法。

   如果指定的检查不受支持，则会引发 "LZMAError"。

   压缩设置可被指定为一个预设的压缩等级（通过 *preset* 参数）或以自定
   义过滤器链来详细设置（通过 *filters* 参数）。

   *preset* 参数（如果提供）应当为一个 "0" 到 "9" (包括边界) 之间的整
   数，可以选择与常数 "PRESET_EXTREME" 进行 OR 运算。 如果 *preset* 和
   *filters* 均未给出，则默认行为是使用 "PRESET_DEFAULT" (预设等级
   "6")。 更高的预设等级会产生更小的输出，但会使得压缩过程更缓慢。

   注解:

     除了更加 CPU 密集，使用更高的预设等级来压缩还需要更多的内存（并产
     生需要更多内存来解压缩的输出）。 例如使用预设等级 "9" 时，一个
     "LZMACompressor" 对象的开销可以高达 800 MiB。 出于这样的原因，通
     常最好是保持使用默认预设等级。

   *filters* 参数（如果提供）应当指定一个过滤器链。 详情参见 指定自定
   义的过滤器链。

   compress(data)

      压缩 *data* (一个 "bytes" object)，返回包含针对输入的至少一部分
      已压缩数据的 "bytes" 对象。 一部 *data* 可能会被放入内部缓冲区，
      以便用于后续的 "compress()" 和 "flush()" 调用。 返回的数据应当与
      之前任何 "compress()" 调用的输出进行拼接。

   flush()

      结束压缩进程，返回包含保存在压缩器的内部缓冲区中的任意数据的
      "bytes" 对象。

      调用此方法之后压缩器将不可再被使用。

class lzma.LZMADecompressor(format=FORMAT_AUTO, memlimit=None, filters=None)

   创建一个压缩器对象，此对象可被用来执行增量解压缩。

   一次性解压缩整个压缩数据流的更便捷方式请参阅 "decompress()"。

   *format* 参数指定应当被使用的容器格式。 默认值为 "FORMAT_AUTO"，它
   可以解压缩 ".xz" 和 ".lzma" 文件。 其他可能的值为 "FORMAT_XZ",
   "FORMAT_ALONE" 和 "FORMAT_RAW"。

   *memlimit* 参数指定解压缩器可以使用的内存上限（字节数）。 当使用此
   参数时，如果不可能在给定内存上限之内解压缩输入数据则解压缩将失败并
   引发 "LZMAError"。

   *filters* 参数指定用于创建被解压缩数据流的过滤器链。 此参数在
   *format* 为 "FORMAT_RAW" 时要求提供，但对于其他格式不应使用。 有关
   过滤器链的更多信息请参阅 指定自定义的过滤器链。

   注解:

     这个类不会透明地处理包含多个已压缩数据流的输入，这不同于
     "decompress()" 和 "LZMAFile"。 要通过 "LZMADecompressor" 来解压缩
     多个数据流输入，你必须为每个数据流都创建一个新的解压缩器。

   decompress(data, max_length=-1)

      解压缩 *data* (一个 *bytes-like object*)，返回字节串形式的解压缩
      数据。 某些 *data* 可以在内部被缓冲，以便用于后续的
      "decompress()" 调用。 返回的数据应当与之前任何 "decompress()" 调
      用的输出进行拼接。

      如果 *max_length* 为非负数，将返回至多 *max_length* 个字节的解压
      缩数据。 如果达到此限制并且可以产生后续输出，则 "needs_input" 属
      性将被设为 "False"。 在这种情况下，下一次 "decompress()" 调用提
      供的 *data* 可以为 "b''" 以获取更多的输出。

      如果所有输入数据都已被解压缩并返回（或是因为它少于 *max_length*
      个字节，或是因为 *max_length* 为负数），则 "needs_input" 属性将
      被设为 "True"。

      在到达数据流末尾之后再尝试解压缩数据会引发 *EOFError*。 在数据流
      末尾之后获取的任何数据都会被忽略并存储至 "unused_data" 属性。

      在 3.5 版更改: 添加了 *max_length* 形参。

   check

      输入流使用的一致性检查的 ID。 这可能为 "CHECK_UNKNOWN" 直到已解
      压了足够的输入数据来确定它所使用的一致性检查。

   eof

      若达到了数据流末尾标识符则为 "True"。

   unused_data

      压缩数据流的末尾还有数据。

      在达到数据流末尾之前，这个值将为 "b"""。

   needs_input

      如果在要求新的未解压缩输入之前 "decompress()" 方法可以提供更多的
      解压缩数据则为 "False"。

      3.5 新版功能.

lzma.compress(data, format=FORMAT_XZ, check=-1, preset=None, filters=None)

   压缩 *data* (一个 "bytes" 对象)，返回包含压缩数据的 "bytes" 对象。

   参见上文的 "LZMACompressor" 了解有关 *format*, *check*, *preset* 和
   *filters* 参数的说明。

lzma.decompress(data, format=FORMAT_AUTO, memlimit=None, filters=None)

   解压缩 *data* (一个 "bytes" 对象)，返回包含解压缩数据的 "bytes" 对
   象。

   如果 *data* 是多个单独压缩数据流的拼接，则解压缩所有相应数据流，并
   返回结果的拼接。

   参见上文的 "LZMADecompressor" 了解有关 *format*, *memlimit* 和
   *filters* 参数的说明。


杂项
====

lzma.is_check_supported(check)

   如果本系统支持给定的一致性检查则返回 "True"。

   "CHECK_NONE" 和 "CHECK_CRC32" 总是受支持。 "CHECK_CRC64" 和
   "CHECK_SHA256" 或许不可用，如果你正在使用基于受限制特性集编译的
   **liblzma** 版本的话。


指定自定义的过滤器链
====================

过滤器链描述符是由字典组成的序列，其中每个字典包含单个过滤器的 ID 和选
项。 每个字典必须包含键 ""id""，并可能包含额外的键用来指定基于过滤器的
选项。 有效的过滤器 ID 如下：

* 压缩过滤器：
     * "FILTER_LZMA1" (配合 "FORMAT_ALONE" 使用)

     * "FILTER_LZMA2" (配合 "FORMAT_XZ" 和 "FORMAT_RAW" 使用)

* Delta 过滤器：
     * "FILTER_DELTA"

* Branch-Call-Jump (BCJ) 过滤器：
     * "FILTER_X86"

     * "FILTER_IA64"

     * "FILTER_ARM"

     * "FILTER_ARMTHUMB"

     * "FILTER_POWERPC"

     * "FILTER_SPARC"

一个过滤器链最多可由 4 个过滤器组成，并且不能为空。 过滤器链中的最后一
个过滤器必须为压缩过滤器，其他过滤器必须为 Delta 或 BCJ 过滤器。

压缩过滤器支持下列选项（指定为表示过滤器的字典中的附加条目）：

   * "preset": 压缩预设选项，用于作为未显式指定的选项的默认值的来源。

   * "dict_size": 以字节表示的字典大小。 这应当在 4 KiB 和 1.5 GiB 之
     间（包含边界）。

   * "lc": 字面值上下文的比特数。

   * "lp": 字面值位置的比特数。 总计值 "lc + lp" 必须不大于 4。

   * "pb": 位置的比特数；必须不大于 4。

   * "mode": "MODE_FAST" 或 "MODE_NORMAL"。

   * "nice_len": 对于一个匹配应当被视为“适宜长度”的值。 这应当小于或等
     于 273。

   * "mf": 要使用的匹配查找器 -- "MF_HC3", "MF_HC4", "MF_BT2",
     "MF_BT3" 或 "MF_BT4"。

   * "depth": 匹配查找器使用的最大查找深度。 0 (默认值) 表示基于其他过
     滤器选项自动选择。

Delta 过滤器保存字节数据之间的差值，在特定环境下可产生更具重复性的输入
。 它支持一个 "dist" 选项，指明要减去的字节之间的差值大小。 默认值为 1
，即相邻字节之间的差值。

BCJ 过滤器主要作用于机器码。 它们会转换机器码内的相对分支、调用和跳转
以使用绝对寻址，其目标是提升冗余度以供压缩器利用。 这些过滤器支持一个
"start_offset" 选项，指明应当被映射到输入数据开头的地址。 默认值为 0。


示例
====

在已压缩的数据中读取:

   import lzma
   with lzma.open("file.xz") as f:
       file_content = f.read()

创建一个压缩文件:

   import lzma
   data = b"Insert Data Here"
   with lzma.open("file.xz", "w") as f:
       f.write(data)

在内存中压缩文件:

   import lzma
   data_in = b"Insert Data Here"
   data_out = lzma.compress(data_in)

增量压缩:

   import lzma
   lzc = lzma.LZMACompressor()
   out1 = lzc.compress(b"Some data\n")
   out2 = lzc.compress(b"Another piece of data\n")
   out3 = lzc.compress(b"Even more data\n")
   out4 = lzc.flush()
   # Concatenate all the partial results:
   result = b"".join([out1, out2, out3, out4])

写入已压缩数据到已打开的文件:

   import lzma
   with open("file.xz", "wb") as f:
       f.write(b"This data will not be compressed\n")
       with lzma.open(f, "w") as lzf:
           lzf.write(b"This *will* be compressed\n")
       f.write(b"Not compressed\n")

使用自定义过滤器链创建一个已压缩文件:

   import lzma
   my_filters = [
       {"id": lzma.FILTER_DELTA, "dist": 5},
       {"id": lzma.FILTER_LZMA2, "preset": 7 | lzma.PRESET_EXTREME},
   ]
   with lzma.open("file.xz", "w", filters=my_filters) as f:
       f.write(b"blah blah blah")
