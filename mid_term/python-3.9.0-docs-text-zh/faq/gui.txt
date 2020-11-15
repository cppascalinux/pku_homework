图形用户界面（GUI）常见问题
***************************


图形界面常见问题
================


Python 是否有平台无关的图形界面工具包？
=======================================

针对不同的（操作系统或）平台，有多种工具包可供选择。虽然有些工具包还没
有移植到 Python 3 上，但至少目前 Tkinter 以及 Qt 是兼容 Python 3 的。


Tkinter
-------

Python 的标准编译包含了 tkinter。这是一个面向对象的接口，指向  Tcl/Tk
微件包。 该接口大概是最容易安装（因为该接口包含在 Python 的大部分 二进
制发行版 中）和使用的工具包。要了解 Tk 的详情，比如源代码等，可访问
Tcl/Tk 项目主页。 Tcl/Tk 可完整移植至 Mac OS X，Windows 和 Unix 操作系
统上。


wxWidgets
---------

wxWidgets (https://www.wxwidgets.org) 是一个自由、可移植的 GUI 图形用
户界面类库，使用 C++ 编写。它可以在多个操作系统平台上提供原生自然的界
面观感。包括Windows、Mac OS X、 GTK 和 X11 平台在内，都是wxWidgets 当
前稳定支持的平台。在语言绑定适配方面，wxWidgets 类库可用于较多语言，包
括 Python，Perl，Ruby等。

wxPython 是 wxWidgets 的 Python 适配。虽然该绑定在更新进度上经常会稍稍
落后于 wxWidgets，但它利用纯 Python 扩展，提供了许多其他语言绑定没有实
现的特性。wxPython 有一个活跃的用户和开发者社区。

wxWidgets 和 wxPython 都是自由开源库。宽松的许可证允许人们在商业软件、
自由软件和共享软件中使用它们。


Qt
--

Qt 工具包 (可使用 PyQt 或 PySide) 及 KDE (PyKDE4) 有多个绑定适配可供选
择。 PyQt 当前相较 PySide 更成熟，但如果你想编写专有软件，就必须要从
Riverbank Computing 购买 PyQt 许可证。 PySide 则可以自由使用于各类软件
。

Qt 4.5 以上版本使用 LGPL 进行许可；此外，商业许可证可从 Qt 公司 那里获
得。


Gtk+
----

针对 Python 的 GObject 内省绑定 可以用于编写 GTK+ 3 应用。 另请参阅
Python GTK+ 3 教程。

更早的、针对 Gtk+ 2 工具包 的 PyGtk 绑定，是由 James Henstridge 实现的
。具体请参考 <http://www.pygtk.org>。


Kivy
----

Kivy 是一种跨平台图形用户界面库，同时支持桌面操作系统（Windows，macOS
和 Linux）以及移动设备（Android，iOS）。该库使用 Python 和 Cython 编写
，可以使用一系列窗口后端。

Kivy 是自由的开源软件，使用 MIT 许可证分发。


FLTK
----

the FLTK toolkit 的Python绑定是简单却功能强大且成熟的跨平台窗口系统，
可以在  the PyFLTK project 里获得相关信息。


OpenGL
------

对于OpenGL绑定，请参阅 PyOpenGL。


有哪些Python的GUI工具是某个平台专用的？
=======================================

通过安装 PyObjc Objective-C bridge，Python程序可以使用Mac OS X的Cocoa
库。

Mark Hammond的 Pythonwin 包括一个微软基础类(MFC)的接口和一个绝大多数由
使用MFC类的Python写成的Python编程环境。


有关Tkinter的问题
=================


我怎样“冻结”Tkinter程序？
-------------------------

Freeze是一个用来创建独立应用程序的工具。 当冻结(freeze) Tkinter程序时
，程序并不是真的能够独立运行，因为程序仍然需要Tcl和Tk库。

一种解决方法是将程序与 Tcl 和 Tk 库一同发布，并且在运行时使用环境变量
"TCL_LIBRARY" 和 "TK_LIBRARY" 指向他们的位置。

为了获得真正能独立运行的应用程序，来自库里的 Tcl 脚本也需要被整合进应
用程序。 一个做这种事情的工具叫 SAM (stand-alone modules，独立模块) ，
它是 Tix distribution (http://tix.sourceforge.net/) 的一部分。

在启用 SAM 时编译 Tix ，在 Python 文件  "Modules/tkappinit.c" 中执行对
"Tclsam_init()" 等的适当调用，并且将程序与 libtclsam 和 libtksam 相链
接（可能也要包括 Tix 的库）。


在等待 I/O 操作时能够处理 Tk 事件吗？
-------------------------------------

在 Windows 以外的其他平台上可以，你甚至不需要使用线程！ 但是你必须稍微
修改一下你的 I/O 代码。 Tk 有与 Xt 的 "XtAddInput()" 对应的调用，它允
许你注册一个回调函数，当一个文件描述符可以进行 I/O 操作的时候，Tk 主循
环将会调用这个回调函数。 参见 File Handlers。


在Tkinter中键绑定不工作：为什么？
---------------------------------

经常听到的抱怨是：已经通过  "bind()" 方法绑定了事件的处理程序，但是，
当按下相关的按键后，这个处理程序却没有执行。

最常见的原因是，那个绑定的控件没有“键盘焦点”。请在 Tk 文档中查找 focus
指令。通常一个控件要获得“键盘焦点”，需要点击那个控件（而不是标签；请查
看 takefocus 选项）。
