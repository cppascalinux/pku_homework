描述符对象
**********

“描述符”是描述对象的某些属性的对象。它们存在于类型对象的字典中。

PyTypeObject PyProperty_Type

   内建描述符类型的类型对象。

PyObject* PyDescr_NewGetSet(PyTypeObject *type, struct PyGetSetDef *getset)
    *Return value: New reference.*

PyObject* PyDescr_NewMember(PyTypeObject *type, struct PyMemberDef *meth)
    *Return value: New reference.*

PyObject* PyDescr_NewMethod(PyTypeObject *type, struct PyMethodDef *meth)
    *Return value: New reference.*

PyObject* PyDescr_NewWrapper(PyTypeObject *type, struct wrapperbase *wrapper, void *wrapped)
    *Return value: New reference.*

PyObject* PyDescr_NewClassMethod(PyTypeObject *type, PyMethodDef *method)
    *Return value: New reference.*

int PyDescr_IsData(PyObject *descr)

   如果描述符对象 *descr* 描述数据属性，则返回true；如果描述方法，则返
   回false。 *descr* 必须是描述符对象；没有错误检查。

PyObject* PyWrapper_New(PyObject *, PyObject *)
    *Return value: New reference.*
