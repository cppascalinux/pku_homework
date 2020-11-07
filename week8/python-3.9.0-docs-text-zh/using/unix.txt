2. 在Unix平台中使用Python
*************************


2.1. 获取最新版本的Python
=========================


2.1.1. 在Linux中
----------------

Python预装在大多数Linux发行版上，并作为一个包提供给所有其他用户。 但是
，您可能想要使用的某些功能在发行版提供的软件包中不可用。这时您可以从源
代码轻松编译最新版本的Python。

如果Python没有预先安装并且不在发行版提供的库中，您可以轻松地为自己使用
的发行版创建包。 参阅以下链接：

参见:

  https://www.debian.org/doc/manuals/maint-guide/first.en.html
     对于Debian用户

  https://en.opensuse.org/Portal:Packaging
     对于OpenSuse用户

  https://docs-old.fedoraproject.org/en-
  US/Fedora_Draft_Documentation/0.1/html/RPM_Guide/ch-creating-
  rpms.html
     对于Fedora用户

  http://www.slackbook.org/html/package-management-making-
  packages.html
     对于Slackware用户


2.1.2. 在FreeBSD和OpenBSD上
---------------------------

* FreeBSD用户，使用以下命令添加包:

     pkg install python3

* OpenBSD用户，使用以下命令添加包:

     pkg_add -r python

     pkg_add ftp://ftp.openbsd.org/pub/OpenBSD/4.2/packages/<insert your architecture here>/python-<version>.tgz

  例如：i386用户获取Python 2.5.1的可用版本:

     pkg_add ftp://ftp.openbsd.org/pub/OpenBSD/4.2/packages/i386/python-2.5.1p2.tgz


2.1.3. 在OpenSolaris系统上
--------------------------

你可以从 OpenCSW 获取、安装及使用各种版本的Python。比如 "pkgutil -i
python27" 。


2.2. 构建Python
===============

如果你想自己编译CPython，首先要做的是获取 source 。您可以下载最新版本
的源代码，也可以直接提取最新的 clone 。 （如果你想要制作补丁，则需要克
隆代码。）

构建过程由常用命令组成：

   ./configure
   make
   make install

特定Unix平台的配置选项和注意事项通常记录在Python源代码的根目录下的
README.rst 文件中。

警告:

  "make install" 可以覆盖或伪装 "python3" 二进制文件。因此，建议使用
  "make altinstall" 而不是 "make install" ，因为后者只安装了
  "*exec_prefix*/bin/python*version*" 。


2.3. 与Python相关的路径和文件
=============================

这取决于本地安装惯例； "prefix" （ "${prefix}" ）和 "exec_prefix" （
"${exec_prefix}" ）  取决于安装，应解释为GNU软件；它们可能相同。

例如，在大多数Linux系统上，两者的默认值是 "/usr" 。

+-------------------------------------------------+--------------------------------------------+
| 文件/目录                                       | 含义                                       |
|=================================================|============================================|
| "*exec_prefix*/bin/python3"                     | 解释器的推荐位置                           |
+-------------------------------------------------+--------------------------------------------+
| "*prefix*/lib/python*version*",                 | 包含标准模块的目录的推荐位置               |
| "*exec_prefix*/lib/python*version*"             |                                            |
+-------------------------------------------------+--------------------------------------------+
| "*prefix*/include/python*version*",             | 包含开发Python扩展和嵌入解释器所需的       |
| "*exec_prefix*/include/python*version*"         | include文件的目录的推荐位置                |
+-------------------------------------------------+--------------------------------------------+


2.4. 杂项
=========

要在Unix上使用Python脚本，需要添加可执行权限，例如：

   $ chmod +x script

并在脚本的顶部放置一个合适的Shebang线。一个很好的选择通常是:

   #!/usr/bin/env python3

将在整个 "PATH" 中搜索Python解释器。但是，某些Unix系统可能没有 **env**
命令，因此可能需要将 "/usr/bin/python3" 硬编码为解释器路径。

要在Python脚本中使用shell命令，请查看 "subprocess" 模块。
