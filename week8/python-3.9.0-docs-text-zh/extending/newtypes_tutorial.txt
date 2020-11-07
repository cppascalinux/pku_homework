2. 自定义扩展类型：教程
***********************

Python 允许编写 C 扩展模块定义可以从 Python 代码中操纵的新类型，这很像
内置的 "str" 和 "list" 类型。所有扩展类型的代码都遵循一个模式，但是在
您开始之前，您需要了解一些细节。这份文件是对这个主题介绍。


2.1. 基础
=========

*CPython* 运行时将所有 Python 对象都视为类型 "PyObject*" 的变量，即所
有 Python 对象的"基础类型"。 "PyObject" 结构体本身包含了对象的
*reference count* 和对象的"类型对象"。 类型对象确定解释器需要调用哪些
(C) 函数，例如一个属性查询一个对象，一个方法调用，或者与另一个对象相乘
。 这些 C 函数被称为“类型方法”。

所以，如果你想要定义新的扩展类型，需要创建新的类型对象。

这类事情只能用例子解释，这里用一个最小化但完整的的模块，定义了新的类型
叫做 "Custom" 在C扩展模块 "custom" 里。

注解:

  这里展示的方法是定义 *static* 扩展类型的传统方法。可以适合大部分用途
  。C API也可以定义在堆上分配的扩展类型，使用 "PyType_FromSpec()" 函数
  ，但不在本入门里讨论。

   #define PY_SSIZE_T_CLEAN
   #include <Python.h>

   typedef struct {
       PyObject_HEAD
       /* Type-specific fields go here. */
   } CustomObject;

   static PyTypeObject CustomType = {
       PyVarObject_HEAD_INIT(NULL, 0)
       .tp_name = "custom.Custom",
       .tp_doc = "Custom objects",
       .tp_basicsize = sizeof(CustomObject),
       .tp_itemsize = 0,
       .tp_flags = Py_TPFLAGS_DEFAULT,
       .tp_new = PyType_GenericNew,
   };

   static PyModuleDef custommodule = {
       PyModuleDef_HEAD_INIT,
       .m_name = "custom",
       .m_doc = "Example module that creates an extension type.",
       .m_size = -1,
   };

   PyMODINIT_FUNC
   PyInit_custom(void)
   {
       PyObject *m;
       if (PyType_Ready(&CustomType) < 0)
           return NULL;

       m = PyModule_Create(&custommodule);
       if (m == NULL)
           return NULL;

       Py_INCREF(&CustomType);
       if (PyModule_AddObject(m, "Custom", (PyObject *) &CustomType) < 0) {
           Py_DECREF(&CustomType);
           Py_DECREF(m);
           return NULL;
       }

       return m;
   }

这部分很容易理解，这是为了跟上一章能对接上。这个文件定义了三件事：

1. "Custom" 类的对象 **object** 包含了： "CustomObject" 结构，这会为每
   个 "Custom" 实例分配一次。

2. "Custom" **type** 的行为：这是 "CustomType" 结构体，其定义了一堆标
   识和函数指针，会指向解释器里请求的操作。

3. 初始化 "custom" 模块： "PyInit_custom" 函数和对应的 "custommodule"
   结构体。

结构的第一块是

   typedef struct {
       PyObject_HEAD
   } CustomObject;

这就是一个自定义对象所包含的。 "PyObject_HEAD" 是强制要求必须在每个对
象结构体之前，用以定义一个类型为 "PyObject" 的字段叫 "ob_base" ，包含
了一个指针指向类型对象和一个引用计数(这可以用宏 "Py_REFCNT" 和
"Py_TYPE" 来区分)。用宏来抽象，使得附加字段可以用调试构建。

注解:

  注意在宏 "PyObject_HEAD" 后没有分号。意外添加分号会导致编译器提示出
  错。

当然，对象除了在 "PyObject_HEAD" 存储数据外，还有额外数据；例如，如下
定义了标准的Python浮点数:

   typedef struct {
       PyObject_HEAD
       double ob_fval;
   } PyFloatObject;

第二个位是类型对象的定义:

   static PyTypeObject CustomType = {
       PyVarObject_HEAD_INIT(NULL, 0)
       .tp_name = "custom.Custom",
       .tp_doc = "Custom objects",
       .tp_basicsize = sizeof(CustomObject),
       .tp_itemsize = 0,
       .tp_flags = Py_TPFLAGS_DEFAULT,
       .tp_new = PyType_GenericNew,
   };

注解:

  推荐使用如上C99风格的初始化，以避免列出所有的 "PyTypeObject" 字段，
  其中很多是你不需要关心的，这样也可以避免关注字段的定义顺序。

在 "object.h" 中实际定义的 "PyTypeObject" 具有比如上定义更多的 字段。
剩余的字段会由 C 编译器用零来填充，通常的做法是不显式地指定它们，除非
你确实需要它们。

我们先挑选一部分，每次一个字段:

   PyVarObject_HEAD_INIT(NULL, 0)

这一行是强制的样板，用以初始化如上提到的 "ob_base" 字段:

   .tp_name = "custom.Custom",

我们的类型的名称。 这将出现在我们的对象的默认文本表示形式和某些错误消
息中，例如:

   >>> "" + custom.Custom()
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
   TypeError: can only concatenate str (not "custom.Custom") to str

Note that the name is a dotted name that includes both the module name
and the name of the type within the module. The module in this case is
"custom" and the type is "Custom", so we set the type name to
"custom.Custom". Using the real dotted import path is important to
make your type compatible with the "pydoc" and "pickle" modules.

   .tp_basicsize = sizeof(CustomObject),
   .tp_itemsize = 0,

This is so that Python knows how much memory to allocate when creating
new "Custom" instances.  "tp_itemsize" is only used for variable-sized
objects and should otherwise be zero.

注解:

  If you want your type to be subclassable from Python, and your type
  has the same "tp_basicsize" as its base type, you may have problems
  with multiple inheritance.  A Python subclass of your type will have
  to list your type first in its "__bases__", or else it will not be
  able to call your type's "__new__()" method without getting an
  error.  You can avoid this problem by ensuring that your type has a
  larger value for "tp_basicsize" than its base type does.  Most of
  the time, this will be true anyway, because either your base type
  will be "object", or else you will be adding data members to your
  base type, and therefore increasing its size.

We set the class flags to "Py_TPFLAGS_DEFAULT".

   .tp_flags = Py_TPFLAGS_DEFAULT,

All types should include this constant in their flags.  It enables all
of the members defined until at least Python 3.3.  If you need further
members, you will need to OR the corresponding flags.

We provide a doc string for the type in "tp_doc".

   .tp_doc = "Custom objects",

To enable object creation, we have to provide a "tp_new" handler.
This is the equivalent of the Python method "__new__()", but has to be
specified explicitly.  In this case, we can just use the default
implementation provided by the API function "PyType_GenericNew()".

   .tp_new = PyType_GenericNew,

Everything else in the file should be familiar, except for some code
in "PyInit_custom()":

   if (PyType_Ready(&CustomType) < 0)
       return;

This initializes the "Custom" type, filling in a number of members to
the appropriate default values, including "ob_type" that we initially
set to "NULL".

   Py_INCREF(&CustomType);
   if (PyModule_AddObject(m, "Custom", (PyObject *) &CustomType) < 0) {
       Py_DECREF(&CustomType);
       Py_DECREF(m);
       return NULL;
   }

This adds the type to the module dictionary.  This allows us to create
"Custom" instances by calling the "Custom" class:

   >>> import custom
   >>> mycustom = custom.Custom()

That's it!  All that remains is to build it; put the above code in a
file called "custom.c" and:

   from distutils.core import setup, Extension
   setup(name="custom", version="1.0",
         ext_modules=[Extension("custom", ["custom.c"])])

in a file called "setup.py"; then typing

   $ python setup.py build

at a shell should produce a file "custom.so" in a subdirectory; move
to that directory and fire up Python --- you should be able to "import
custom" and play around with Custom objects.

That wasn't so hard, was it?

Of course, the current Custom type is pretty uninteresting. It has no
data and doesn't do anything. It can't even be subclassed.

注解:

  While this documentation showcases the standard "distutils" module
  for building C extensions, it is recommended in real-world use cases
  to use the newer and better-maintained "setuptools" library.
  Documentation on how to do this is out of scope for this document
  and can be found in the Python Packaging User's Guide.


2.2. Adding data and methods to the Basic example
=================================================

Let's extend the basic example to add some data and methods.  Let's
also make the type usable as a base class. We'll create a new module,
"custom2" that adds these capabilities:

   #define PY_SSIZE_T_CLEAN
   #include <Python.h>
   #include "structmember.h"

   typedef struct {
       PyObject_HEAD
       PyObject *first; /* first name */
       PyObject *last;  /* last name */
       int number;
   } CustomObject;

   static void
   Custom_dealloc(CustomObject *self)
   {
       Py_XDECREF(self->first);
       Py_XDECREF(self->last);
       Py_TYPE(self)->tp_free((PyObject *) self);
   }

   static PyObject *
   Custom_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
   {
       CustomObject *self;
       self = (CustomObject *) type->tp_alloc(type, 0);
       if (self != NULL) {
           self->first = PyUnicode_FromString("");
           if (self->first == NULL) {
               Py_DECREF(self);
               return NULL;
           }
           self->last = PyUnicode_FromString("");
           if (self->last == NULL) {
               Py_DECREF(self);
               return NULL;
           }
           self->number = 0;
       }
       return (PyObject *) self;
   }

   static int
   Custom_init(CustomObject *self, PyObject *args, PyObject *kwds)
   {
       static char *kwlist[] = {"first", "last", "number", NULL};
       PyObject *first = NULL, *last = NULL, *tmp;

       if (!PyArg_ParseTupleAndKeywords(args, kwds, "|OOi", kwlist,
                                        &first, &last,
                                        &self->number))
           return -1;

       if (first) {
           tmp = self->first;
           Py_INCREF(first);
           self->first = first;
           Py_XDECREF(tmp);
       }
       if (last) {
           tmp = self->last;
           Py_INCREF(last);
           self->last = last;
           Py_XDECREF(tmp);
       }
       return 0;
   }

   static PyMemberDef Custom_members[] = {
       {"first", T_OBJECT_EX, offsetof(CustomObject, first), 0,
        "first name"},
       {"last", T_OBJECT_EX, offsetof(CustomObject, last), 0,
        "last name"},
       {"number", T_INT, offsetof(CustomObject, number), 0,
        "custom number"},
       {NULL}  /* Sentinel */
   };

   static PyObject *
   Custom_name(CustomObject *self, PyObject *Py_UNUSED(ignored))
   {
       if (self->first == NULL) {
           PyErr_SetString(PyExc_AttributeError, "first");
           return NULL;
       }
       if (self->last == NULL) {
           PyErr_SetString(PyExc_AttributeError, "last");
           return NULL;
       }
       return PyUnicode_FromFormat("%S %S", self->first, self->last);
   }

   static PyMethodDef Custom_methods[] = {
       {"name", (PyCFunction) Custom_name, METH_NOARGS,
        "Return the name, combining the first and last name"
       },
       {NULL}  /* Sentinel */
   };

   static PyTypeObject CustomType = {
       PyVarObject_HEAD_INIT(NULL, 0)
       .tp_name = "custom2.Custom",
       .tp_doc = "Custom objects",
       .tp_basicsize = sizeof(CustomObject),
       .tp_itemsize = 0,
       .tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
       .tp_new = Custom_new,
       .tp_init = (initproc) Custom_init,
       .tp_dealloc = (destructor) Custom_dealloc,
       .tp_members = Custom_members,
       .tp_methods = Custom_methods,
   };

   static PyModuleDef custommodule = {
       PyModuleDef_HEAD_INIT,
       .m_name = "custom2",
       .m_doc = "Example module that creates an extension type.",
       .m_size = -1,
   };

   PyMODINIT_FUNC
   PyInit_custom2(void)
   {
       PyObject *m;
       if (PyType_Ready(&CustomType) < 0)
           return NULL;

       m = PyModule_Create(&custommodule);
       if (m == NULL)
           return NULL;

       Py_INCREF(&CustomType);
       if (PyModule_AddObject(m, "Custom", (PyObject *) &CustomType) < 0) {
           Py_DECREF(&CustomType);
           Py_DECREF(m);
           return NULL;
       }

       return m;
   }

This version of the module has a number of changes.

We've added an extra include:

   #include <structmember.h>

This include provides declarations that we use to handle attributes,
as described a bit later.

The  "Custom" type now has three data attributes in its C struct,
*first*, *last*, and *number*.  The *first* and *last* variables are
Python strings containing first and last names.  The *number*
attribute is a C integer.

The object structure is updated accordingly:

   typedef struct {
       PyObject_HEAD
       PyObject *first; /* first name */
       PyObject *last;  /* last name */
       int number;
   } CustomObject;

Because we now have data to manage, we have to be more careful about
object allocation and deallocation.  At a minimum, we need a
deallocation method:

   static void
   Custom_dealloc(CustomObject *self)
   {
       Py_XDECREF(self->first);
       Py_XDECREF(self->last);
       Py_TYPE(self)->tp_free((PyObject *) self);
   }

which is assigned to the "tp_dealloc" member:

   .tp_dealloc = (destructor) Custom_dealloc,

This method first clears the reference counts of the two Python
attributes. "Py_XDECREF()" correctly handles the case where its
argument is "NULL" (which might happen here if "tp_new" failed
midway).  It then calls the "tp_free" member of the object's type
(computed by "Py_TYPE(self)") to free the object's memory.  Note that
the object's type might not be "CustomType", because the object may be
an instance of a subclass.

注解:

  The explicit cast to "destructor" above is needed because we defined
  "Custom_dealloc" to take a "CustomObject *" argument, but the
  "tp_dealloc" function pointer expects to receive a "PyObject *"
  argument.  Otherwise, the compiler will emit a warning.  This is
  object-oriented polymorphism, in C!

We want to make sure that the first and last names are initialized to
empty strings, so we provide a "tp_new" implementation:

   static PyObject *
   Custom_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
   {
       CustomObject *self;
       self = (CustomObject *) type->tp_alloc(type, 0);
       if (self != NULL) {
           self->first = PyUnicode_FromString("");
           if (self->first == NULL) {
               Py_DECREF(self);
               return NULL;
           }
           self->last = PyUnicode_FromString("");
           if (self->last == NULL) {
               Py_DECREF(self);
               return NULL;
           }
           self->number = 0;
       }
       return (PyObject *) self;
   }

and install it in the "tp_new" member:

   .tp_new = Custom_new,

The "tp_new" handler is responsible for creating (as opposed to
initializing) objects of the type.  It is exposed in Python as the
"__new__()" method. It is not required to define a "tp_new" member,
and indeed many extension types will simply reuse
"PyType_GenericNew()" as done in the first version of the "Custom"
type above.  In this case, we use the "tp_new" handler to initialize
the "first" and "last" attributes to non-"NULL" default values.

"tp_new" is passed the type being instantiated (not necessarily
"CustomType", if a subclass is instantiated) and any arguments passed
when the type was called, and is expected to return the instance
created.  "tp_new" handlers always accept positional and keyword
arguments, but they often ignore the arguments, leaving the argument
handling to initializer (a.k.a. "tp_init" in C or "__init__" in
Python) methods.

注解:

  "tp_new" shouldn't call "tp_init" explicitly, as the interpreter
  will do it itself.

The "tp_new" implementation calls the "tp_alloc" slot to allocate
memory:

   self = (CustomObject *) type->tp_alloc(type, 0);

Since memory allocation may fail, we must check the "tp_alloc" result
against "NULL" before proceeding.

注解:

  We didn't fill the "tp_alloc" slot ourselves. Rather
  "PyType_Ready()" fills it for us by inheriting it from our base
  class, which is "object" by default.  Most types use the default
  allocation strategy.

注解:

  If you are creating a co-operative "tp_new" (one that calls a base
  type's "tp_new" or "__new__()"), you must *not* try to determine
  what method to call using method resolution order at runtime.
  Always statically determine what type you are going to call, and
  call its "tp_new" directly, or via "type->tp_base->tp_new".  If you
  do not do this, Python subclasses of your type that also inherit
  from other Python-defined classes may not work correctly.
  (Specifically, you may not be able to create instances of such
  subclasses without getting a "TypeError".)

We also define an initialization function which accepts arguments to
provide initial values for our instance:

   static int
   Custom_init(CustomObject *self, PyObject *args, PyObject *kwds)
   {
       static char *kwlist[] = {"first", "last", "number", NULL};
       PyObject *first = NULL, *last = NULL, *tmp;

       if (!PyArg_ParseTupleAndKeywords(args, kwds, "|OOi", kwlist,
                                        &first, &last,
                                        &self->number))
           return -1;

       if (first) {
           tmp = self->first;
           Py_INCREF(first);
           self->first = first;
           Py_XDECREF(tmp);
       }
       if (last) {
           tmp = self->last;
           Py_INCREF(last);
           self->last = last;
           Py_XDECREF(tmp);
       }
       return 0;
   }

by filling the "tp_init" slot.

   .tp_init = (initproc) Custom_init,

The "tp_init" slot is exposed in Python as the "__init__()" method.
It is used to initialize an object after it's created.  Initializers
always accept positional and keyword arguments, and they should return
either "0" on success or "-1" on error.

Unlike the "tp_new" handler, there is no guarantee that "tp_init" is
called at all (for example, the "pickle" module by default doesn't
call "__init__()" on unpickled instances).  It can also be called
multiple times.  Anyone can call the "__init__()" method on our
objects.  For this reason, we have to be extra careful when assigning
the new attribute values.  We might be tempted, for example to assign
the "first" member like this:

   if (first) {
       Py_XDECREF(self->first);
       Py_INCREF(first);
       self->first = first;
   }

But this would be risky.  Our type doesn't restrict the type of the
"first" member, so it could be any kind of object.  It could have a
destructor that causes code to be executed that tries to access the
"first" member; or that destructor could release the *Global
interpreter Lock* and let arbitrary code run in other threads that
accesses and modifies our object.

To be paranoid and protect ourselves against this possibility, we
almost always reassign members before decrementing their reference
counts.  When don't we have to do this?

* when we absolutely know that the reference count is greater than 1;

* when we know that deallocation of the object [1] will neither
  release the *GIL* nor cause any calls back into our type's code;

* when decrementing a reference count in a "tp_dealloc" handler on a
  type which doesn't support cyclic garbage collection [2].

We want to expose our instance variables as attributes. There are a
number of ways to do that. The simplest way is to define member
definitions:

   static PyMemberDef Custom_members[] = {
       {"first", T_OBJECT_EX, offsetof(CustomObject, first), 0,
        "first name"},
       {"last", T_OBJECT_EX, offsetof(CustomObject, last), 0,
        "last name"},
       {"number", T_INT, offsetof(CustomObject, number), 0,
        "custom number"},
       {NULL}  /* Sentinel */
   };

and put the definitions in the "tp_members" slot:

   .tp_members = Custom_members,

Each member definition has a member name, type, offset, access flags
and documentation string.  See the 泛型属性管理 section below for
details.

A disadvantage of this approach is that it doesn't provide a way to
restrict the types of objects that can be assigned to the Python
attributes.  We expect the first and last names to be strings, but any
Python objects can be assigned. Further, the attributes can be
deleted, setting the C pointers to "NULL".  Even though we can make
sure the members are initialized to non-"NULL" values, the members can
be set to "NULL" if the attributes are deleted.

We define a single method, "Custom.name()", that outputs the objects
name as the concatenation of the first and last names.

   static PyObject *
   Custom_name(CustomObject *self, PyObject *Py_UNUSED(ignored))
   {
       if (self->first == NULL) {
           PyErr_SetString(PyExc_AttributeError, "first");
           return NULL;
       }
       if (self->last == NULL) {
           PyErr_SetString(PyExc_AttributeError, "last");
           return NULL;
       }
       return PyUnicode_FromFormat("%S %S", self->first, self->last);
   }

The method is implemented as a C function that takes a "Custom" (or
"Custom" subclass) instance as the first argument.  Methods always
take an instance as the first argument. Methods often take positional
and keyword arguments as well, but in this case we don't take any and
don't need to accept a positional argument tuple or keyword argument
dictionary. This method is equivalent to the Python method:

   def name(self):
       return "%s %s" % (self.first, self.last)

Note that we have to check for the possibility that our "first" and
"last" members are "NULL".  This is because they can be deleted, in
which case they are set to "NULL".  It would be better to prevent
deletion of these attributes and to restrict the attribute values to
be strings.  We'll see how to do that in the next section.

Now that we've defined the method, we need to create an array of
method definitions:

   static PyMethodDef Custom_methods[] = {
       {"name", (PyCFunction) Custom_name, METH_NOARGS,
        "Return the name, combining the first and last name"
       },
       {NULL}  /* Sentinel */
   };

(note that we used the "METH_NOARGS" flag to indicate that the method
is expecting no arguments other than *self*)

and assign it to the "tp_methods" slot:

   .tp_methods = Custom_methods,

Finally, we'll make our type usable as a base class for subclassing.
We've written our methods carefully so far so that they don't make any
assumptions about the type of the object being created or used, so all
we need to do is to add the "Py_TPFLAGS_BASETYPE" to our class flag
definition:

   .tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,

We rename "PyInit_custom()" to "PyInit_custom2()", update the module
name in the "PyModuleDef" struct, and update the full class name in
the "PyTypeObject" struct.

Finally, we update our "setup.py" file to build the new module:

   from distutils.core import setup, Extension
   setup(name="custom", version="1.0",
         ext_modules=[
            Extension("custom", ["custom.c"]),
            Extension("custom2", ["custom2.c"]),
            ])


2.3. Providing finer control over data attributes
=================================================

In this section, we'll provide finer control over how the "first" and
"last" attributes are set in the "Custom" example. In the previous
version of our module, the instance variables "first" and "last" could
be set to non-string values or even deleted. We want to make sure that
these attributes always contain strings.

   #define PY_SSIZE_T_CLEAN
   #include <Python.h>
   #include "structmember.h"

   typedef struct {
       PyObject_HEAD
       PyObject *first; /* first name */
       PyObject *last;  /* last name */
       int number;
   } CustomObject;

   static void
   Custom_dealloc(CustomObject *self)
   {
       Py_XDECREF(self->first);
       Py_XDECREF(self->last);
       Py_TYPE(self)->tp_free((PyObject *) self);
   }

   static PyObject *
   Custom_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
   {
       CustomObject *self;
       self = (CustomObject *) type->tp_alloc(type, 0);
       if (self != NULL) {
           self->first = PyUnicode_FromString("");
           if (self->first == NULL) {
               Py_DECREF(self);
               return NULL;
           }
           self->last = PyUnicode_FromString("");
           if (self->last == NULL) {
               Py_DECREF(self);
               return NULL;
           }
           self->number = 0;
       }
       return (PyObject *) self;
   }

   static int
   Custom_init(CustomObject *self, PyObject *args, PyObject *kwds)
   {
       static char *kwlist[] = {"first", "last", "number", NULL};
       PyObject *first = NULL, *last = NULL, *tmp;

       if (!PyArg_ParseTupleAndKeywords(args, kwds, "|UUi", kwlist,
                                        &first, &last,
                                        &self->number))
           return -1;

       if (first) {
           tmp = self->first;
           Py_INCREF(first);
           self->first = first;
           Py_DECREF(tmp);
       }
       if (last) {
           tmp = self->last;
           Py_INCREF(last);
           self->last = last;
           Py_DECREF(tmp);
       }
       return 0;
   }

   static PyMemberDef Custom_members[] = {
       {"number", T_INT, offsetof(CustomObject, number), 0,
        "custom number"},
       {NULL}  /* Sentinel */
   };

   static PyObject *
   Custom_getfirst(CustomObject *self, void *closure)
   {
       Py_INCREF(self->first);
       return self->first;
   }

   static int
   Custom_setfirst(CustomObject *self, PyObject *value, void *closure)
   {
       PyObject *tmp;
       if (value == NULL) {
           PyErr_SetString(PyExc_TypeError, "Cannot delete the first attribute");
           return -1;
       }
       if (!PyUnicode_Check(value)) {
           PyErr_SetString(PyExc_TypeError,
                           "The first attribute value must be a string");
           return -1;
       }
       tmp = self->first;
       Py_INCREF(value);
       self->first = value;
       Py_DECREF(tmp);
       return 0;
   }

   static PyObject *
   Custom_getlast(CustomObject *self, void *closure)
   {
       Py_INCREF(self->last);
       return self->last;
   }

   static int
   Custom_setlast(CustomObject *self, PyObject *value, void *closure)
   {
       PyObject *tmp;
       if (value == NULL) {
           PyErr_SetString(PyExc_TypeError, "Cannot delete the last attribute");
           return -1;
       }
       if (!PyUnicode_Check(value)) {
           PyErr_SetString(PyExc_TypeError,
                           "The last attribute value must be a string");
           return -1;
       }
       tmp = self->last;
       Py_INCREF(value);
       self->last = value;
       Py_DECREF(tmp);
       return 0;
   }

   static PyGetSetDef Custom_getsetters[] = {
       {"first", (getter) Custom_getfirst, (setter) Custom_setfirst,
        "first name", NULL},
       {"last", (getter) Custom_getlast, (setter) Custom_setlast,
        "last name", NULL},
       {NULL}  /* Sentinel */
   };

   static PyObject *
   Custom_name(CustomObject *self, PyObject *Py_UNUSED(ignored))
   {
       return PyUnicode_FromFormat("%S %S", self->first, self->last);
   }

   static PyMethodDef Custom_methods[] = {
       {"name", (PyCFunction) Custom_name, METH_NOARGS,
        "Return the name, combining the first and last name"
       },
       {NULL}  /* Sentinel */
   };

   static PyTypeObject CustomType = {
       PyVarObject_HEAD_INIT(NULL, 0)
       .tp_name = "custom3.Custom",
       .tp_doc = "Custom objects",
       .tp_basicsize = sizeof(CustomObject),
       .tp_itemsize = 0,
       .tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
       .tp_new = Custom_new,
       .tp_init = (initproc) Custom_init,
       .tp_dealloc = (destructor) Custom_dealloc,
       .tp_members = Custom_members,
       .tp_methods = Custom_methods,
       .tp_getset = Custom_getsetters,
   };

   static PyModuleDef custommodule = {
       PyModuleDef_HEAD_INIT,
       .m_name = "custom3",
       .m_doc = "Example module that creates an extension type.",
       .m_size = -1,
   };

   PyMODINIT_FUNC
   PyInit_custom3(void)
   {
       PyObject *m;
       if (PyType_Ready(&CustomType) < 0)
           return NULL;

       m = PyModule_Create(&custommodule);
       if (m == NULL)
           return NULL;

       Py_INCREF(&CustomType);
       if (PyModule_AddObject(m, "Custom", (PyObject *) &CustomType) < 0) {
           Py_DECREF(&CustomType);
           Py_DECREF(m);
           return NULL;
       }

       return m;
   }

To provide greater control, over the "first" and "last" attributes,
we'll use custom getter and setter functions.  Here are the functions
for getting and setting the "first" attribute:

   static PyObject *
   Custom_getfirst(CustomObject *self, void *closure)
   {
       Py_INCREF(self->first);
       return self->first;
   }

   static int
   Custom_setfirst(CustomObject *self, PyObject *value, void *closure)
   {
       PyObject *tmp;
       if (value == NULL) {
           PyErr_SetString(PyExc_TypeError, "Cannot delete the first attribute");
           return -1;
       }
       if (!PyUnicode_Check(value)) {
           PyErr_SetString(PyExc_TypeError,
                           "The first attribute value must be a string");
           return -1;
       }
       tmp = self->first;
       Py_INCREF(value);
       self->first = value;
       Py_DECREF(tmp);
       return 0;
   }

The getter function is passed a "Custom" object and a "closure", which
is a void pointer.  In this case, the closure is ignored.  (The
closure supports an advanced usage in which definition data is passed
to the getter and setter. This could, for example, be used to allow a
single set of getter and setter functions that decide the attribute to
get or set based on data in the closure.)

The setter function is passed the "Custom" object, the new value, and
the closure.  The new value may be "NULL", in which case the attribute
is being deleted.  In our setter, we raise an error if the attribute
is deleted or if its new value is not a string.

We create an array of "PyGetSetDef" structures:

   static PyGetSetDef Custom_getsetters[] = {
       {"first", (getter) Custom_getfirst, (setter) Custom_setfirst,
        "first name", NULL},
       {"last", (getter) Custom_getlast, (setter) Custom_setlast,
        "last name", NULL},
       {NULL}  /* Sentinel */
   };

and register it in the "tp_getset" slot:

   .tp_getset = Custom_getsetters,

The last item in a "PyGetSetDef" structure is the "closure" mentioned
above.  In this case, we aren't using a closure, so we just pass
"NULL".

We also remove the member definitions for these attributes:

   static PyMemberDef Custom_members[] = {
       {"number", T_INT, offsetof(CustomObject, number), 0,
        "custom number"},
       {NULL}  /* Sentinel */
   };

We also need to update the "tp_init" handler to only allow strings [3]
to be passed:

   static int
   Custom_init(CustomObject *self, PyObject *args, PyObject *kwds)
   {
       static char *kwlist[] = {"first", "last", "number", NULL};
       PyObject *first = NULL, *last = NULL, *tmp;

       if (!PyArg_ParseTupleAndKeywords(args, kwds, "|UUi", kwlist,
                                        &first, &last,
                                        &self->number))
           return -1;

       if (first) {
           tmp = self->first;
           Py_INCREF(first);
           self->first = first;
           Py_DECREF(tmp);
       }
       if (last) {
           tmp = self->last;
           Py_INCREF(last);
           self->last = last;
           Py_DECREF(tmp);
       }
       return 0;
   }

With these changes, we can assure that the "first" and "last" members
are never "NULL" so we can remove checks for "NULL" values in almost
all cases. This means that most of the "Py_XDECREF()" calls can be
converted to "Py_DECREF()" calls.  The only place we can't change
these calls is in the "tp_dealloc" implementation, where there is the
possibility that the initialization of these members failed in
"tp_new".

We also rename the module initialization function and module name in
the initialization function, as we did before, and we add an extra
definition to the "setup.py" file.


2.4. Supporting cyclic garbage collection
=========================================

Python has a *cyclic garbage collector (GC)* that can identify
unneeded objects even when their reference counts are not zero. This
can happen when objects are involved in cycles.  For example,
consider:

   >>> l = []
   >>> l.append(l)
   >>> del l

In this example, we create a list that contains itself. When we delete
it, it still has a reference from itself. Its reference count doesn't
drop to zero. Fortunately, Python's cyclic garbage collector will
eventually figure out that the list is garbage and free it.

In the second version of the "Custom" example, we allowed any kind of
object to be stored in the "first" or "last" attributes [4]. Besides,
in the second and third versions, we allowed subclassing "Custom", and
subclasses may add arbitrary attributes.  For any of those two
reasons, "Custom" objects can participate in cycles:

   >>> import custom3
   >>> class Derived(custom3.Custom): pass
   ...
   >>> n = Derived()
   >>> n.some_attribute = n

To allow a "Custom" instance participating in a reference cycle to be
properly detected and collected by the cyclic GC, our "Custom" type
needs to fill two additional slots and to enable a flag that enables
these slots:

   #define PY_SSIZE_T_CLEAN
   #include <Python.h>
   #include "structmember.h"

   typedef struct {
       PyObject_HEAD
       PyObject *first; /* first name */
       PyObject *last;  /* last name */
       int number;
   } CustomObject;

   static int
   Custom_traverse(CustomObject *self, visitproc visit, void *arg)
   {
       Py_VISIT(self->first);
       Py_VISIT(self->last);
       return 0;
   }

   static int
   Custom_clear(CustomObject *self)
   {
       Py_CLEAR(self->first);
       Py_CLEAR(self->last);
       return 0;
   }

   static void
   Custom_dealloc(CustomObject *self)
   {
       PyObject_GC_UnTrack(self);
       Custom_clear(self);
       Py_TYPE(self)->tp_free((PyObject *) self);
   }

   static PyObject *
   Custom_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
   {
       CustomObject *self;
       self = (CustomObject *) type->tp_alloc(type, 0);
       if (self != NULL) {
           self->first = PyUnicode_FromString("");
           if (self->first == NULL) {
               Py_DECREF(self);
               return NULL;
           }
           self->last = PyUnicode_FromString("");
           if (self->last == NULL) {
               Py_DECREF(self);
               return NULL;
           }
           self->number = 0;
       }
       return (PyObject *) self;
   }

   static int
   Custom_init(CustomObject *self, PyObject *args, PyObject *kwds)
   {
       static char *kwlist[] = {"first", "last", "number", NULL};
       PyObject *first = NULL, *last = NULL, *tmp;

       if (!PyArg_ParseTupleAndKeywords(args, kwds, "|UUi", kwlist,
                                        &first, &last,
                                        &self->number))
           return -1;

       if (first) {
           tmp = self->first;
           Py_INCREF(first);
           self->first = first;
           Py_DECREF(tmp);
       }
       if (last) {
           tmp = self->last;
           Py_INCREF(last);
           self->last = last;
           Py_DECREF(tmp);
       }
       return 0;
   }

   static PyMemberDef Custom_members[] = {
       {"number", T_INT, offsetof(CustomObject, number), 0,
        "custom number"},
       {NULL}  /* Sentinel */
   };

   static PyObject *
   Custom_getfirst(CustomObject *self, void *closure)
   {
       Py_INCREF(self->first);
       return self->first;
   }

   static int
   Custom_setfirst(CustomObject *self, PyObject *value, void *closure)
   {
       if (value == NULL) {
           PyErr_SetString(PyExc_TypeError, "Cannot delete the first attribute");
           return -1;
       }
       if (!PyUnicode_Check(value)) {
           PyErr_SetString(PyExc_TypeError,
                           "The first attribute value must be a string");
           return -1;
       }
       Py_INCREF(value);
       Py_CLEAR(self->first);
       self->first = value;
       return 0;
   }

   static PyObject *
   Custom_getlast(CustomObject *self, void *closure)
   {
       Py_INCREF(self->last);
       return self->last;
   }

   static int
   Custom_setlast(CustomObject *self, PyObject *value, void *closure)
   {
       if (value == NULL) {
           PyErr_SetString(PyExc_TypeError, "Cannot delete the last attribute");
           return -1;
       }
       if (!PyUnicode_Check(value)) {
           PyErr_SetString(PyExc_TypeError,
                           "The last attribute value must be a string");
           return -1;
       }
       Py_INCREF(value);
       Py_CLEAR(self->last);
       self->last = value;
       return 0;
   }

   static PyGetSetDef Custom_getsetters[] = {
       {"first", (getter) Custom_getfirst, (setter) Custom_setfirst,
        "first name", NULL},
       {"last", (getter) Custom_getlast, (setter) Custom_setlast,
        "last name", NULL},
       {NULL}  /* Sentinel */
   };

   static PyObject *
   Custom_name(CustomObject *self, PyObject *Py_UNUSED(ignored))
   {
       return PyUnicode_FromFormat("%S %S", self->first, self->last);
   }

   static PyMethodDef Custom_methods[] = {
       {"name", (PyCFunction) Custom_name, METH_NOARGS,
        "Return the name, combining the first and last name"
       },
       {NULL}  /* Sentinel */
   };

   static PyTypeObject CustomType = {
       PyVarObject_HEAD_INIT(NULL, 0)
       .tp_name = "custom4.Custom",
       .tp_doc = "Custom objects",
       .tp_basicsize = sizeof(CustomObject),
       .tp_itemsize = 0,
       .tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE | Py_TPFLAGS_HAVE_GC,
       .tp_new = Custom_new,
       .tp_init = (initproc) Custom_init,
       .tp_dealloc = (destructor) Custom_dealloc,
       .tp_traverse = (traverseproc) Custom_traverse,
       .tp_clear = (inquiry) Custom_clear,
       .tp_members = Custom_members,
       .tp_methods = Custom_methods,
       .tp_getset = Custom_getsetters,
   };

   static PyModuleDef custommodule = {
       PyModuleDef_HEAD_INIT,
       .m_name = "custom4",
       .m_doc = "Example module that creates an extension type.",
       .m_size = -1,
   };

   PyMODINIT_FUNC
   PyInit_custom4(void)
   {
       PyObject *m;
       if (PyType_Ready(&CustomType) < 0)
           return NULL;

       m = PyModule_Create(&custommodule);
       if (m == NULL)
           return NULL;

       Py_INCREF(&CustomType);
       if (PyModule_AddObject(m, "Custom", (PyObject *) &CustomType) < 0) {
           Py_DECREF(&CustomType);
           Py_DECREF(m);
           return NULL;
       }

       return m;
   }

First, the traversal method lets the cyclic GC know about subobjects
that could participate in cycles:

   static int
   Custom_traverse(CustomObject *self, visitproc visit, void *arg)
   {
       int vret;
       if (self->first) {
           vret = visit(self->first, arg);
           if (vret != 0)
               return vret;
       }
       if (self->last) {
           vret = visit(self->last, arg);
           if (vret != 0)
               return vret;
       }
       return 0;
   }

For each subobject that can participate in cycles, we need to call the
"visit()" function, which is passed to the traversal method. The
"visit()" function takes as arguments the subobject and the extra
argument *arg* passed to the traversal method.  It returns an integer
value that must be returned if it is non-zero.

Python provides a "Py_VISIT()" macro that automates calling visit
functions.  With "Py_VISIT()", we can minimize the amount of
boilerplate in "Custom_traverse":

   static int
   Custom_traverse(CustomObject *self, visitproc visit, void *arg)
   {
       Py_VISIT(self->first);
       Py_VISIT(self->last);
       return 0;
   }

注解:

  The "tp_traverse" implementation must name its arguments exactly
  *visit* and *arg* in order to use "Py_VISIT()".

Second, we need to provide a method for clearing any subobjects that
can participate in cycles:

   static int
   Custom_clear(CustomObject *self)
   {
       Py_CLEAR(self->first);
       Py_CLEAR(self->last);
       return 0;
   }

Notice the use of the "Py_CLEAR()" macro.  It is the recommended and
safe way to clear data attributes of arbitrary types while
decrementing their reference counts.  If you were to call
"Py_XDECREF()" instead on the attribute before setting it to "NULL",
there is a possibility that the attribute's destructor would call back
into code that reads the attribute again (*especially* if there is a
reference cycle).

注解:

  You could emulate "Py_CLEAR()" by writing:

     PyObject *tmp;
     tmp = self->first;
     self->first = NULL;
     Py_XDECREF(tmp);

  Nevertheless, it is much easier and less error-prone to always use
  "Py_CLEAR()" when deleting an attribute.  Don't try to micro-
  optimize at the expense of robustness!

The deallocator "Custom_dealloc" may call arbitrary code when clearing
attributes.  It means the circular GC can be triggered inside the
function. Since the GC assumes reference count is not zero, we need to
untrack the object from the GC by calling "PyObject_GC_UnTrack()"
before clearing members. Here is our reimplemented deallocator using
"PyObject_GC_UnTrack()" and "Custom_clear":

   static void
   Custom_dealloc(CustomObject *self)
   {
       PyObject_GC_UnTrack(self);
       Custom_clear(self);
       Py_TYPE(self)->tp_free((PyObject *) self);
   }

Finally, we add the "Py_TPFLAGS_HAVE_GC" flag to the class flags:

   .tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE | Py_TPFLAGS_HAVE_GC,

That's pretty much it.  If we had written custom "tp_alloc" or
"tp_free" handlers, we'd need to modify them for cyclic garbage
collection.  Most extensions will use the versions automatically
provided.


2.5. Subclassing other types
============================

It is possible to create new extension types that are derived from
existing types. It is easiest to inherit from the built in types,
since an extension can easily use the "PyTypeObject" it needs. It can
be difficult to share these "PyTypeObject" structures between
extension modules.

In this example we will create a "SubList" type that inherits from the
built-in "list" type. The new type will be completely compatible with
regular lists, but will have an additional "increment()" method that
increases an internal counter:

   >>> import sublist
   >>> s = sublist.SubList(range(3))
   >>> s.extend(s)
   >>> print(len(s))
   6
   >>> print(s.increment())
   1
   >>> print(s.increment())
   2

   #define PY_SSIZE_T_CLEAN
   #include <Python.h>

   typedef struct {
       PyListObject list;
       int state;
   } SubListObject;

   static PyObject *
   SubList_increment(SubListObject *self, PyObject *unused)
   {
       self->state++;
       return PyLong_FromLong(self->state);
   }

   static PyMethodDef SubList_methods[] = {
       {"increment", (PyCFunction) SubList_increment, METH_NOARGS,
        PyDoc_STR("increment state counter")},
       {NULL},
   };

   static int
   SubList_init(SubListObject *self, PyObject *args, PyObject *kwds)
   {
       if (PyList_Type.tp_init((PyObject *) self, args, kwds) < 0)
           return -1;
       self->state = 0;
       return 0;
   }

   static PyTypeObject SubListType = {
       PyVarObject_HEAD_INIT(NULL, 0)
       .tp_name = "sublist.SubList",
       .tp_doc = "SubList objects",
       .tp_basicsize = sizeof(SubListObject),
       .tp_itemsize = 0,
       .tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
       .tp_init = (initproc) SubList_init,
       .tp_methods = SubList_methods,
   };

   static PyModuleDef sublistmodule = {
       PyModuleDef_HEAD_INIT,
       .m_name = "sublist",
       .m_doc = "Example module that creates an extension type.",
       .m_size = -1,
   };

   PyMODINIT_FUNC
   PyInit_sublist(void)
   {
       PyObject *m;
       SubListType.tp_base = &PyList_Type;
       if (PyType_Ready(&SubListType) < 0)
           return NULL;

       m = PyModule_Create(&sublistmodule);
       if (m == NULL)
           return NULL;

       Py_INCREF(&SubListType);
       if (PyModule_AddObject(m, "SubList", (PyObject *) &SubListType) < 0) {
           Py_DECREF(&SubListType);
           Py_DECREF(m);
           return NULL;
       }

       return m;
   }

As you can see, the source code closely resembles the "Custom"
examples in previous sections. We will break down the main differences
between them.

   typedef struct {
       PyListObject list;
       int state;
   } SubListObject;

The primary difference for derived type objects is that the base
type's object structure must be the first value.  The base type will
already include the "PyObject_HEAD()" at the beginning of its
structure.

When a Python object is a "SubList" instance, its "PyObject *" pointer
can be safely cast to both "PyListObject *" and "SubListObject *":

   static int
   SubList_init(SubListObject *self, PyObject *args, PyObject *kwds)
   {
       if (PyList_Type.tp_init((PyObject *) self, args, kwds) < 0)
           return -1;
       self->state = 0;
       return 0;
   }

We see above how to call through to the "__init__" method of the base
type.

This pattern is important when writing a type with custom "tp_new" and
"tp_dealloc" members.  The "tp_new" handler should not actually create
the memory for the object with its "tp_alloc", but let the base class
handle it by calling its own "tp_new".

The "PyTypeObject" struct supports a "tp_base" specifying the type's
concrete base class.  Due to cross-platform compiler issues, you can't
fill that field directly with a reference to "PyList_Type"; it should
be done later in the module initialization function:

   PyMODINIT_FUNC
   PyInit_sublist(void)
   {
       PyObject* m;
       SubListType.tp_base = &PyList_Type;
       if (PyType_Ready(&SubListType) < 0)
           return NULL;

       m = PyModule_Create(&sublistmodule);
       if (m == NULL)
           return NULL;

       Py_INCREF(&SubListType);
       if (PyModule_AddObject(m, "SubList", (PyObject *) &SubListType) < 0) {
           Py_DECREF(&SubListType);
           Py_DECREF(m);
           return NULL;
       }

       return m;
   }

Before calling "PyType_Ready()", the type structure must have the
"tp_base" slot filled in.  When we are deriving an existing type, it
is not necessary to fill out the "tp_alloc" slot with
"PyType_GenericNew()" -- the allocation function from the base type
will be inherited.

After that, calling "PyType_Ready()" and adding the type object to the
module is the same as with the basic "Custom" examples.

-[ 脚注 ]-

[1] This is true when we know that the object is a basic type, like a
    string or a float.

[2] We relied on this in the "tp_dealloc" handler in this example,
    because our type doesn't support garbage collection.

[3] We now know that the first and last members are strings, so
    perhaps we could be less careful about decrementing their
    reference counts, however, we accept instances of string
    subclasses.  Even though deallocating normal strings won't call
    back into our objects, we can't guarantee that deallocating an
    instance of a string subclass won't call back into our objects.

[4] Also, even with our attributes restricted to strings instances,
    the user could pass arbitrary "str" subclasses and therefore still
    create reference cycles.
