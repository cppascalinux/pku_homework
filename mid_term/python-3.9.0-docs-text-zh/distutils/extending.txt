7. 扩展 Distutils
*****************

注解:

  这篇文档只有在
  https://setuptools.readthedocs.io/en/latest/setuptools.html 上的
  "setuptools" 文档独立涵盖此处包含的所有相关信息之前，才会单独保留。

Distutils 可以通过各种方式扩展。 大多数扩展都采用新命令或现有命令的替
换形式。 例如，可以编写新命令以支持新的特定于平台的包格式，但是可以修
改现有命令的替换，以修改命令在包上的操作细节。

distutils 的大多数扩展都在想要修改现有命令的 "setup.py" 脚本中编写；其
中许多只是简单地在 ".py" 文件以外添加了一些应当被拷贝到包中的文件后缀
以便使用。

大多部 distutils 命令的实现都是 "distutils.cmd.Command" 类的子类。 新
增命令可直接继承自 "Command"，而替换命令往往间接派生自 "Command"， 直
接子类化它们所替换的命令。 所有命令都要求自 "Command" 派生。


7.1. 集成新的命令
=================

有多种方法可将新的命令实现集成到 distutils 中。 最困难的一种是鼓动在
distutils 自身内部包含新特性，并等待（以及要求）某个 Python 版本提供该
支持。 出于多种原因，这确实是相当难的。

对于大多数需求来说最为常见并且可能最为合理的一种则是通过你自己的
"setup.py" 脚本来包含新的实现，然后让 "distutils.core.setup()" 函数使
用它们:

   from distutils.command.build_py import build_py as _build_py
   from distutils.core import setup

   class build_py(_build_py):
       """Specialized Python source builder."""

       # implement whatever needs to be different...

   setup(cmdclass={'build_py': build_py},
         ...)

如果新的实现必须通过特定的包来使用则此方式最为适宜，因为每个对这个包感
兴趣的人都将会需要有新的命令实现。

从 Python 2.4 开始，还有第三个选项可用，其目标是允许添加支持现有
"setup.py" 脚本的新命令，而不需要修改 Python 安装包。 这预计可允许第三
方扩展提供对附加打包系统的支持，而相应命令又可用于任何 distutils 命令
可被使用的地方。 新的配置选项 "command_packages" (命令行选项为 "--
command-packages") 可用来指定附加包，以在其中查找实现新增命令的模块。
像所有 distutils 选项一样，这可以通过命令行或配置文件来指定。 此选项只
能在配置文件的 "[global]" 小节之中或在命令行的任何命令之前设置。 如果
是设置在配置文件中，则它可被命令行设置重载；如果在命令行中将其设为空字
符串则将会使用默认值。 此选项绝不应当在随特定包提供的配置文件中设置。

这个新选项可被用来添加任意数量的包到查找命令实现的包列表；多个包名应当
以逗号分隔。 当未指明时，查找将只在 "distutils.command" 包中进行。 但
是当 "setup.py" 附带 "--command-packages distcmds,buildcmds" 选项运行
时，"distutils.command", "distcmds" 和 "buildcmds" 包将按此顺序被查找
。 新的命令应当在与命名同名的模块中由同名的类来实现。 给定上述示例命令
行选项，则命令 **bdist_openpkg** 可由类
"distcmds.bdist_openpkg.bdist_openpkg" 或
"buildcmds.bdist_openpkg.bdist_openpkg" 来实现。


7.2. 添加新的发布类型
=====================

创建发布（在 "dist/" 目录中的文件）的命令需要将 "(command, filename)"
二元组添加到 "self.distribution.dist_files" 以便 **upload** 可以将其上
传到 PyPI。 二元组中的 *filename* 不包含路径信息而只有文件名本身。 在
dry-run 模式下，二元组仍然应当被添加以表示必须创建的内容。
