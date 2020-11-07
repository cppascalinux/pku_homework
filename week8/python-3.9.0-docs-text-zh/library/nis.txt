"nis" --- Sun 的 NIS (黄页) 接口
********************************

======================================================================

"nis" 模块提供了对 NIS 库的轻量级包装，适用于多个主机的集中管理。

因为 NIS 仅存在于 Unix 系统，此模块仅在 Unix 上可用。

"nis" 模块定义了以下函数：

nis.match(key, mapname, domain=default_domain)

   返回 *key* 在映射 *mapname* 中的匹配结果，如无结果则会引发错误
   ("nis.error")。 两个参数都应为字符串，*key* 定长 8 个比特。 返回值
   为任意字节数组（可包含 "NULL" 和其他特殊值）。

   请注意如果 *mapname* 是另一名称的别名则会先检查别名。

   *domain* 参数可允许重载用于查找的 NIS 域。 如果未指定，则会在默认
   NIS 域中查找。

nis.cat(mapname, domain=default_domain)

   返回一个字典，其元素为 *key* 到 *value* 的映射使得 "match(key,
   mapname)==value"。 请注意字典的键和值均为任意字节数组。

   请注意如果 *mapname* 是另一名称的别名则会先检查别名。

   *domain* 参数可允许重载用于查找的 NIS 域。 如果未指定，则会在默认
   NIS 域中查找。

nis.maps(domain=default_domain)

   返回全部可用映射的列表。

   *domain* 参数可允许重载用于查找的 NIS 域。 如果未指定，则会在默认
   NIS 域中查找。

nis.get_default_domain()

   返回系统默认的 NIS 域。

"nis" 模块定义了以下异常：

exception nis.error

   当 NIS 函数返回一个错误码时引发的异常。
