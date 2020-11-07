"urllib.robotparser" --- robots.txt 语法分析程序
************************************************

**源代码：** Lib/urllib/robotparser.py

======================================================================

此模块提供了一个单独的类 "RobotFileParser"，它可以回答关于某个特定用户
代理是否能在 Web 站点获取发布 "robots.txt" 文件的 URL 的问题。 有关
"robots.txt" 文件结构的更多细节请参阅
http://www.robotstxt.org/orig.html。

class urllib.robotparser.RobotFileParser(url='')

   这个类提供了一些可以读取、解析和回答关于 *url* 上的 "robots.txt" 文
   件的问题的方法。

   set_url(url)

      设置指向 "robots.txt" 文件的 URL。

   read()

      读取 "robots.txt" URL 并将其输入解析器。

   parse(lines)

      解析行参数。

   can_fetch(useragent, url)

      如果允许 *useragent* 按照被解析 "robots.txt" 文件中的规则来获取
      *url* 则返回 "True"。

   mtime()

      返回最近一次获取 "robots.txt" 文件的时间。 这适用于需要定期检查
      "robots.txt" 文件更新情况的长时间运行的网页爬虫。

   modified()

      将最近一次获取 "robots.txt" 文件的时间设置为当前时间。

   crawl_delay(useragent)

      为指定的 *useragent* 从 "robots.txt" 返回 "Crawl-delay" 形参。
      如果此形参不存在或不适用于指定的 *useragent* 或者此形参的
      "robots.txt" 条目存在语法错误，则返回 "None"。

      3.6 新版功能.

   request_rate(useragent)

      以 *named tuple* "RequestRate(requests, seconds)" 的形式从
      "robots.txt" 返回 "Request-rate" 形参的内容。 如果此形参不存在或
      不适用于指定的 *useragent* 或者此形参的 "robots.txt" 条目存在语
      法错误，则返回 "None"。

      3.6 新版功能.

   site_maps()

      以 "list()" 的形式从 "robots.txt" 返回 "Sitemap" 形参的内容。 如
      果此形参不存在或者此形参的 "robots.txt" 条目存在语法错误，则返回
      "None"。

      3.8 新版功能.

下面的例子演示了 "RobotFileParser" 类的基本用法:

   >>> import urllib.robotparser
   >>> rp = urllib.robotparser.RobotFileParser()
   >>> rp.set_url("http://www.musi-cal.com/robots.txt")
   >>> rp.read()
   >>> rrate = rp.request_rate("*")
   >>> rrate.requests
   3
   >>> rrate.seconds
   20
   >>> rp.crawl_delay("*")
   6
   >>> rp.can_fetch("*", "http://www.musi-cal.com/cgi-bin/search?city=San+Francisco")
   False
   >>> rp.can_fetch("*", "http://www.musi-cal.com/")
   True
