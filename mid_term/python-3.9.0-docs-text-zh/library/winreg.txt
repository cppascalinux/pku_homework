"winreg" --- Windows 注册表访问
*******************************

======================================================================

这些函数将 Windows 注册表 API 暴露给 Python。为了确保即便程序员忽略了
显式关闭句柄，该句柄依然能够正确关闭，它使用了一个 handle 对象 而不是
整数来作为注册表句柄。

在 3.3 版更改: 该模块中的几个函数被用于引发 "WindowsError"，该异常现在
是 "OSError" 的别名。


函数
====

该模块提供了下列函数：

winreg.CloseKey(hkey)

   关闭之前打开的注册表键。参数 *hkey* 指之前打开的键。

   注解:

     如果没有使用该方法关闭 *hkey* (或者通过 "hkey.Close()")，在对象
     *hkey* 被 Python 销毁时会将其关闭。

winreg.ConnectRegistry(computer_name, key)

   建立到另一台计算上上的预定义注册表句柄的连接，并返回一个 handle 对
   象.

   *computer_name* 是远程计算机的名称，以 "r"\\computername"" 的形式。
   如果是 "None" ，将会使用本地计算机。

   *key* 是所连接到的预定义句柄。

   返回值是所开打键的句柄。如果函数失败，则引发一个 "OSError" 异常。

   引发一个 审计事件 "winreg.ConnectRegistry"，附带参数
   "computer_name", "key"。

   在 3.3 版更改: 参考 上文。

winreg.CreateKey(key, sub_key)

   创建或打开特定的键，返回一个 handle 对象。

   *key* 为某个已经打开的键，或者预定义的 HKEY_* 常量 之一。

   *sub_key* 是用于命名该方法所打开或创建的键的字符串。

   如果 *key* 是预定义键之一，*sub_key* 可能会是 "None"。该情况下，返
   回的句柄就是传入函数的句柄。

   如果键已经存在，则该函数打开已经存在的该键。

   返回值是所开打键的句柄。如果函数失败，则引发一个 "OSError" 异常。

   引发一个 审计事件 "winreg.CreateKey"，附带参数 "key", "sub_key",
   "access"。

   引发一个 审计事件 "winreg.OpenKey/result"，附带参数 "key"。

   在 3.3 版更改: 参考 上文。

winreg.CreateKeyEx(key, sub_key, reserved=0, access=KEY_WRITE)

   创建或打开特定的键，返回一个 handle 对象。

   *key* 为某个已经打开的键，或者预定义的 HKEY_* 常量 之一。

   *sub_key* 是用于命名该方法所打开或创建的键的字符串。

   *reserved* 是一个保留的证书，必须是零。默认值为零。

   *access* 为一个整数，用于给键的预期安全访问指定访问掩码。默认值为
   "KEY_WRITE"。 参阅 Access Rights  了解其它允许值。

   如果 *key* 是预定义键之一，*sub_key* 可能会是 "None"。该情况下，返
   回的句柄就是传入函数的句柄。

   如果键已经存在，则该函数打开已经存在的该键。

   返回值是所开打键的句柄。如果函数失败，则引发一个 "OSError" 异常。

   引发一个 审计事件 "winreg.CreateKey"，附带参数 "key", "sub_key",
   "access"。

   引发一个 审计事件 "winreg.OpenKey/result"，附带参数 "key"。

   3.2 新版功能.

   在 3.3 版更改: 参考 上文。

winreg.DeleteKey(key, sub_key)

   删除指定的键。

   *key* 为某个已经打开的键，或者预定义的 HKEY_* 常量 之一。

   *sub_key* 这个字符串必须是由 *key* 参数所指定键的一个子项。该值项不
   可以是 "None"，同时键也不可以有子项。

   *该方法不能删除带有子项的键。*

   如果方法成功，则整个键，包括其所有值项都会被移除。如果方法失败，则
   引发一个 "OSError" 异常。

   引发一个 审计事件 "winreg.DeleteKey"，附带参数 "key", "sub_key",
   "access"。

   在 3.3 版更改: 参考 上文。

winreg.DeleteKeyEx(key, sub_key, access=KEY_WOW64_64KEY, reserved=0)

   删除指定的键。

   注解:

     函数 "DeleteKeyEx()" 通过 RegDeleteKeyEx 这个 Windows API 函数实
     现，该函数为 Windows 的64位版本专属。 参阅 RegDeleteKeyEx 文档。

   *key* 为某个已经打开的键，或者预定义的 HKEY_* 常量 之一。

   *sub_key* 这个字符串必须是由 *key* 参数所指定键的一个子项。该值项不
   可以是 "None"，同时键也不可以有子项。

   *reserved* 是一个保留的证书，必须是零。默认值为零。

   *access* 为一个整数，用于给键的预期安全访问指定访问掩码。默认值为常
   量 "_WOW64_64KEY" 。参阅 Access Rights  了解其它允许值。

   *该方法不能删除带有子项的键。*

   如果方法成功，则整个键，包括其所有值项都会被移除。如果方法失败，则
   引发一个 "OSError" 异常。

   在不支持的 Windows 版本之上，将会引发 "NotImplementedError" 异常。

   引发一个 审计事件 "winreg.DeleteKey"，附带参数 "key", "sub_key",
   "access"。

   3.2 新版功能.

   在 3.3 版更改: 参考 上文。

winreg.DeleteValue(key, value)

   从某个注册键中删除一个命名值项。

   *key* 为某个已经打开的键，或者预定义的 HKEY_* 常量 之一。

   *value* 为标识所要删除值项的字符串。

   引发一个 审计事件 "winreg.DeleteValue"，附带参数 "key", "value"。

winreg.EnumKey(key, index)

   列举某个已经打开注册表键的子项，并返回一个字符串。

   *key* 为某个已经打开的键，或者预定义的 HKEY_* 常量 之一。

   *index* 为一个整数，用于标识所获取键的索引。

   每次调用该函数都会获取一个子项的名字。通常它会被反复调用，直到引发
   "OSError" 异常，这说明已经没有更多的可用值了。

   引发一个 审计事件 "winreg.EnumKey"，附带参数 "key", "index"。

   在 3.3 版更改: 参考 上文。

winreg.EnumValue(key, index)

   列举某个已经打开注册表键的值项，并返回一个元组。

   *key* 为某个已经打开的键，或者预定义的 HKEY_* 常量 之一。

   *index* 为一个整数，用于标识要获取值项的索引。

   每次调用该函数都会获取一个子项的名字。通常它会被反复调用，直到引发
   "OSError" 异常，这说明已经没有更多的可用值了。

   结果为3元素的元组。

   +---------+----------------------------------------------+
   | 索引    | 意义                                         |
   |=========|==============================================|
   | "0"     | 用于标识值项名称的字符串。                   |
   +---------+----------------------------------------------+
   | "1"     | 保存值项数据的对象，其类型取决于背后的注册表 |
   |         | 类型。                                       |
   +---------+----------------------------------------------+
   | "2"     | 标识值项数据类型的整数。（请查阅             |
   |         | "SetValueEx()" 文档中的表格）                |
   +---------+----------------------------------------------+

   引发一个 审计事件 "winreg.EnumValue"，附带参数 "key", "index"。

   在 3.3 版更改: 参考 上文。

winreg.ExpandEnvironmentStrings(str)

   Expands environment variable placeholders "%NAME%" in strings like
   "REG_EXPAND_SZ":

      >>> ExpandEnvironmentStrings('%windir%')
      'C:\\Windows'

   引发一个 审计事件 "winreg.ExpandEnvironmentStrings"，附带参数 "str"
   。

winreg.FlushKey(key)

   将某个键的所有属性写入注册表。

   *key* 为某个已经打开的键，或者预定义的 HKEY_* 常量 之一。

   It is not necessary to call "FlushKey()" to change a key. Registry
   changes are flushed to disk by the registry using its lazy flusher.
   Registry changes are also flushed to disk at system shutdown.
   Unlike "CloseKey()", the "FlushKey()" method returns only when all
   the data has been written to the registry. An application should
   only call "FlushKey()" if it requires absolute certainty that
   registry changes are on disk.

   注解:

     If you don't know whether a "FlushKey()" call is required, it
     probably isn't.

winreg.LoadKey(key, sub_key, file_name)

   Creates a subkey under the specified key and stores registration
   information from a specified file into that subkey.

   *key* is a handle returned by "ConnectRegistry()" or one of the
   constants "HKEY_USERS" or "HKEY_LOCAL_MACHINE".

   *sub_key* is a string that identifies the subkey to load.

   *file_name* is the name of the file to load registry data from.
   This file must have been created with the "SaveKey()" function.
   Under the file allocation table (FAT) file system, the filename may
   not have an extension.

   A call to "LoadKey()" fails if the calling process does not have
   the "SE_RESTORE_PRIVILEGE" privilege.  Note that privileges are
   different from permissions -- see the RegLoadKey documentation for
   more details.

   If *key* is a handle returned by "ConnectRegistry()", then the path
   specified in *file_name* is relative to the remote computer.

   引发一个 审计事件 "winreg.LoadKey"，附带参数 "key", "sub_key",
   "file_name"。

winreg.OpenKey(key, sub_key, reserved=0, access=KEY_READ)
winreg.OpenKeyEx(key, sub_key, reserved=0, access=KEY_READ)

   Opens the specified key, returning a handle object.

   *key* 为某个已经打开的键，或者预定义的 HKEY_* 常量 之一。

   *sub_key* is a string that identifies the sub_key to open.

   *reserved* is a reserved integer, and must be zero.  The default is
   zero.

   *access* is an integer that specifies an access mask that describes
   the desired security access for the key.  Default is "KEY_READ".
   See Access Rights for other allowed values.

   The result is a new handle to the specified key.

   If the function fails, "OSError" is raised.

   引发一个 审计事件 "winreg.OpenKey"，附带参数 "key", "sub_key",
   "access"。

   引发一个 审计事件 "winreg.OpenKey/result"，附带参数 "key"。

   在 3.2 版更改: Allow the use of named arguments.

   在 3.3 版更改: 参考 上文。

winreg.QueryInfoKey(key)

   Returns information about a key, as a tuple.

   *key* 为某个已经打开的键，或者预定义的 HKEY_* 常量 之一。

   结果为3元素的元组。

   +---------+-----------------------------------------------+
   | 索引    | 意义                                          |
   |=========|===============================================|
   | "0"     | An integer giving the number of sub keys this |
   |         | key has.                                      |
   +---------+-----------------------------------------------+
   | "1"     | An integer giving the number of values this   |
   |         | key has.                                      |
   +---------+-----------------------------------------------+
   | "2"     | An integer giving when the key was last       |
   |         | modified (if available) as 100's of           |
   |         | nanoseconds since Jan 1, 1601.                |
   +---------+-----------------------------------------------+

   引发一个 审计事件 "winreg.QueryInfoKey"，附带参数 "key"。

winreg.QueryValue(key, sub_key)

   Retrieves the unnamed value for a key, as a string.

   *key* 为某个已经打开的键，或者预定义的 HKEY_* 常量 之一。

   *sub_key* is a string that holds the name of the subkey with which
   the value is associated.  If this parameter is "None" or empty, the
   function retrieves the value set by the "SetValue()" method for the
   key identified by *key*.

   Values in the registry have name, type, and data components. This
   method retrieves the data for a key's first value that has a "NULL"
   name. But the underlying API call doesn't return the type, so
   always use "QueryValueEx()" if possible.

   引发一个 审计事件 "winreg.QueryValue"，附带参数 "key", "sub_key",
   "value_name"。

winreg.QueryValueEx(key, value_name)

   Retrieves the type and data for a specified value name associated
   with an open registry key.

   *key* 为某个已经打开的键，或者预定义的 HKEY_* 常量 之一。

   *value_name* is a string indicating the value to query.

   The result is a tuple of 2 items:

   +---------+-------------------------------------------+
   | 索引    | 意义                                      |
   |=========|===========================================|
   | "0"     | The value of the registry item.           |
   +---------+-------------------------------------------+
   | "1"     | An integer giving the registry type for   |
   |         | this value (see table in docs for         |
   |         | "SetValueEx()")                           |
   +---------+-------------------------------------------+

   引发一个 审计事件 "winreg.QueryValue"，附带参数 "key", "sub_key",
   "value_name"。

winreg.SaveKey(key, file_name)

   Saves the specified key, and all its subkeys to the specified file.

   *key* 为某个已经打开的键，或者预定义的 HKEY_* 常量 之一。

   *file_name* is the name of the file to save registry data to.  This
   file cannot already exist. If this filename includes an extension,
   it cannot be used on file allocation table (FAT) file systems by
   the "LoadKey()" method.

   If *key* represents a key on a remote computer, the path described
   by *file_name* is relative to the remote computer. The caller of
   this method must possess the "SeBackupPrivilege" security
   privilege.  Note that privileges are different than permissions --
   see the Conflicts Between User Rights and Permissions documentation
   for more details.

   This function passes "NULL" for *security_attributes* to the API.

   引发一个 审计事件 "winreg.SaveKey"，附带参数 "key", "file_name"。

winreg.SetValue(key, sub_key, type, value)

   Associates a value with a specified key.

   *key* 为某个已经打开的键，或者预定义的 HKEY_* 常量 之一。

   *sub_key* is a string that names the subkey with which the value is
   associated.

   *type* is an integer that specifies the type of the data. Currently
   this must be "REG_SZ", meaning only strings are supported.  Use the
   "SetValueEx()" function for support for other data types.

   *value* is a string that specifies the new value.

   If the key specified by the *sub_key* parameter does not exist, the
   SetValue function creates it.

   Value lengths are limited by available memory. Long values (more
   than 2048 bytes) should be stored as files with the filenames
   stored in the configuration registry.  This helps the registry
   perform efficiently.

   The key identified by the *key* parameter must have been opened
   with "KEY_SET_VALUE" access.

   引发一个 审计事件 "winreg.SetValue"，附带参数 "key", "sub_key",
   "type", "value"。

winreg.SetValueEx(key, value_name, reserved, type, value)

   Stores data in the value field of an open registry key.

   *key* 为某个已经打开的键，或者预定义的 HKEY_* 常量 之一。

   *value_name* is a string that names the subkey with which the value
   is associated.

   *reserved* can be anything -- zero is always passed to the API.

   *type* is an integer that specifies the type of the data. See Value
   Types for the available types.

   *value* is a string that specifies the new value.

   This method can also set additional value and type information for
   the specified key.  The key identified by the key parameter must
   have been opened with "KEY_SET_VALUE" access.

   To open the key, use the "CreateKey()" or "OpenKey()" methods.

   Value lengths are limited by available memory. Long values (more
   than 2048 bytes) should be stored as files with the filenames
   stored in the configuration registry.  This helps the registry
   perform efficiently.

   引发一个 审计事件 "winreg.SetValue"，附带参数 "key", "sub_key",
   "type", "value"。

winreg.DisableReflectionKey(key)

   Disables registry reflection for 32-bit processes running on a
   64-bit operating system.

   *key* 为某个已经打开的键，或者预定义的 HKEY_* 常量 之一。

   Will generally raise "NotImplementedError" if executed on a 32-bit
   operating system.

   If the key is not on the reflection list, the function succeeds but
   has no effect.  Disabling reflection for a key does not affect
   reflection of any subkeys.

   引发一个 审计事件 "winreg.DisableReflectionKey"，附带参数 "key"。

winreg.EnableReflectionKey(key)

   Restores registry reflection for the specified disabled key.

   *key* 为某个已经打开的键，或者预定义的 HKEY_* 常量 之一。

   Will generally raise "NotImplementedError" if executed on a 32-bit
   operating system.

   Restoring reflection for a key does not affect reflection of any
   subkeys.

   引发一个 审计事件 "winreg.EnableReflectionKey"，附带参数 "key"。

winreg.QueryReflectionKey(key)

   Determines the reflection state for the specified key.

   *key* 为某个已经打开的键，或者预定义的 HKEY_* 常量 之一。

   Returns "True" if reflection is disabled.

   Will generally raise "NotImplementedError" if executed on a 32-bit
   operating system.

   引发一个 审计事件 "winreg.QueryReflectionKey"，附带参数 "key"。


常数
====

The following constants are defined for use in many "_winreg"
functions.


HKEY_* Constants
----------------

winreg.HKEY_CLASSES_ROOT

   Registry entries subordinate to this key define types (or classes)
   of documents and the properties associated with those types. Shell
   and COM applications use the information stored under this key.

winreg.HKEY_CURRENT_USER

   Registry entries subordinate to this key define the preferences of
   the current user. These preferences include the settings of
   environment variables, data about program groups, colors, printers,
   network connections, and application preferences.

winreg.HKEY_LOCAL_MACHINE

   Registry entries subordinate to this key define the physical state
   of the computer, including data about the bus type, system memory,
   and installed hardware and software.

winreg.HKEY_USERS

   Registry entries subordinate to this key define the default user
   configuration for new users on the local computer and the user
   configuration for the current user.

winreg.HKEY_PERFORMANCE_DATA

   Registry entries subordinate to this key allow you to access
   performance data. The data is not actually stored in the registry;
   the registry functions cause the system to collect the data from
   its source.

winreg.HKEY_CURRENT_CONFIG

   Contains information about the current hardware profile of the
   local computer system.

winreg.HKEY_DYN_DATA

   This key is not used in versions of Windows after 98.


Access Rights
-------------

For more information, see Registry Key Security and Access.

winreg.KEY_ALL_ACCESS

   Combines the STANDARD_RIGHTS_REQUIRED, "KEY_QUERY_VALUE",
   "KEY_SET_VALUE", "KEY_CREATE_SUB_KEY", "KEY_ENUMERATE_SUB_KEYS",
   "KEY_NOTIFY", and "KEY_CREATE_LINK" access rights.

winreg.KEY_WRITE

   Combines the STANDARD_RIGHTS_WRITE, "KEY_SET_VALUE", and
   "KEY_CREATE_SUB_KEY" access rights.

winreg.KEY_READ

   Combines the STANDARD_RIGHTS_READ, "KEY_QUERY_VALUE",
   "KEY_ENUMERATE_SUB_KEYS", and "KEY_NOTIFY" values.

winreg.KEY_EXECUTE

   Equivalent to "KEY_READ".

winreg.KEY_QUERY_VALUE

   Required to query the values of a registry key.

winreg.KEY_SET_VALUE

   Required to create, delete, or set a registry value.

winreg.KEY_CREATE_SUB_KEY

   Required to create a subkey of a registry key.

winreg.KEY_ENUMERATE_SUB_KEYS

   Required to enumerate the subkeys of a registry key.

winreg.KEY_NOTIFY

   Required to request change notifications for a registry key or for
   subkeys of a registry key.

winreg.KEY_CREATE_LINK

   Reserved for system use.


64-bit Specific
~~~~~~~~~~~~~~~

For more information, see Accessing an Alternate Registry View.

winreg.KEY_WOW64_64KEY

   Indicates that an application on 64-bit Windows should operate on
   the 64-bit registry view.

winreg.KEY_WOW64_32KEY

   Indicates that an application on 64-bit Windows should operate on
   the 32-bit registry view.


Value Types
-----------

For more information, see Registry Value Types.

winreg.REG_BINARY

   Binary data in any form.

winreg.REG_DWORD

   32-bit number.

winreg.REG_DWORD_LITTLE_ENDIAN

   A 32-bit number in little-endian format. Equivalent to "REG_DWORD".

winreg.REG_DWORD_BIG_ENDIAN

   A 32-bit number in big-endian format.

winreg.REG_EXPAND_SZ

   Null-terminated string containing references to environment
   variables ("%PATH%").

winreg.REG_LINK

   A Unicode symbolic link.

winreg.REG_MULTI_SZ

   A sequence of null-terminated strings, terminated by two null
   characters. (Python handles this termination automatically.)

winreg.REG_NONE

   No defined value type.

winreg.REG_QWORD

   A 64-bit number.

   3.6 新版功能.

winreg.REG_QWORD_LITTLE_ENDIAN

   A 64-bit number in little-endian format. Equivalent to "REG_QWORD".

   3.6 新版功能.

winreg.REG_RESOURCE_LIST

   A device-driver resource list.

winreg.REG_FULL_RESOURCE_DESCRIPTOR

   A hardware setting.

winreg.REG_RESOURCE_REQUIREMENTS_LIST

   A hardware resource list.

winreg.REG_SZ

   A null-terminated string.


Registry Handle Objects
=======================

This object wraps a Windows HKEY object, automatically closing it when
the object is destroyed.  To guarantee cleanup, you can call either
the "Close()" method on the object, or the "CloseKey()" function.

All registry functions in this module return one of these objects.

All registry functions in this module which accept a handle object
also accept an integer, however, use of the handle object is
encouraged.

Handle objects provide semantics for "__bool__()" -- thus

   if handle:
       print("Yes")

will print "Yes" if the handle is currently valid (has not been closed
or detached).

The object also support comparison semantics, so handle objects will
compare true if they both reference the same underlying Windows handle
value.

Handle objects can be converted to an integer (e.g., using the built-
in "int()" function), in which case the underlying Windows handle
value is returned.  You can also use the "Detach()" method to return
the integer handle, and also disconnect the Windows handle from the
handle object.

PyHKEY.Close()

   Closes the underlying Windows handle.

   If the handle is already closed, no error is raised.

PyHKEY.Detach()

   Detaches the Windows handle from the handle object.

   The result is an integer that holds the value of the handle before
   it is detached.  If the handle is already detached or closed, this
   will return zero.

   After calling this function, the handle is effectively invalidated,
   but the handle is not closed.  You would call this function when
   you need the underlying Win32 handle to exist beyond the lifetime
   of the handle object.

   引发一个 审计事件 "winreg.PyHKEY.Detach"，附带参数 "key"。

PyHKEY.__enter__()
PyHKEY.__exit__(*exc_info)

   The HKEY object implements "__enter__()" and "__exit__()" and thus
   supports the context protocol for the "with" statement:

      with OpenKey(HKEY_LOCAL_MACHINE, "foo") as key:
          ...  # work with key

   will automatically close *key* when control leaves the "with"
   block.
