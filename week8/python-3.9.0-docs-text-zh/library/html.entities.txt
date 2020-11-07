"html.entities" --- HTML 一般实体的定义
***************************************

**源码：** Lib/html/entities.py

======================================================================

该模块定义了四个词典， "html5"、 "name2codepoint"、 "codepoint2name"、
以及 "entitydefs"。

html.entities.html5

   将 HTML5 命名字符引用 [1] 映射到等效的 Unicode 字符的字典，例如
   "html5['gt;'] == '>'"。 请注意，尾随的分号包含在名称中（例如
   "'gt;'" ），但是即使没有分号，一些名称也会被标准接受，在这种情况下
   ，名称出现时带有和不带有 "';'"。另见 "html.unescape()"。

   3.3 新版功能.

html.entities.entitydefs

   将 XHTML 1.0 实体定义映射到 ISO Latin-1 中的替换文本的字典。

html.entities.name2codepoint

   将 HTML 实体名称映射到 Unicode 代码点的字典。

html.entities.codepoint2name

   将 Unicode 代码点映射到 HTML 实体名称的字典。

-[ 脚注 ]-

[1] 参见 https://www.w3.org/TR/html5/syntax.html#named-character-
    references
