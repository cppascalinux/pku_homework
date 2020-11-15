"asyncore" --- 异步socket处理器
*******************************

**源码：** Lib/asyncore.py

3.6 版后已移除: 请使用 "asyncio" 替代。

======================================================================

注解:

  该模块仅为提供向后兼容。我们推荐在新代码中使用 "asyncio" 。

该模块提供用于编写异步套接字服务客户端与服务端的基础构件。

只有两种方法让单个处理器上的程序“同一时间完成不止一件事”。 多线程编程
是最简单和最流行的方法，但是还有另一种非常不同的技术，它可以让你拥有多
线程的几乎所有优点，而无需实际使用多线程。 它仅仅在你的程序主要受 I/O
限制时有用，那么。 如果你的程序受处理器限制，那么先发制人的预定线程可
能就是你真正需要的。 但是，网络服务器很少受处理器限制。

如果你的操作系统在其 I/O 库中支持 "select()" 系统调用（几乎所有操作系
统），那么你可以使用它来同时处理多个通信通道；在 I/O 正在“后台”时进行
其他工作。 虽然这种策略看起来很奇怪和复杂，特别是起初，它在很多方面比
多线程编程更容易理解和控制。 "asyncore" 模块为您解决了许多难题，使得构
建复杂的高性能网络服务器和客户端的任务变得轻而易举。 对于“会话”应用程
序和协议，伴侣 "asynchat" 模块是非常宝贵的。

这两个模块背后的基本思想是创建一个或多个网络 *通道* ，类的实例
"asyncore.dispatcher" 和 "asynchat.async_chat" 。 创建通道会将它们添加
到全局映射中，如果你不为它提供自己的 *映射* ，则由 "loop()" 函数使用。

一旦创建了初始通道，调用 "loop()" 函数将激活通道服务，该服务将一直持续
到最后一个通道（包括在异步服务期间已添加到映射中的任何通道）关闭。

asyncore.loop([timeout[, use_poll[, map[, count]]]])

   进入一个轮询循环，其在循环计数超出或所有打开的通道关闭后终止。 所有
   参数都是可选的。 *count* 形参默认为 "None" ，导致循环仅在所有通道关
   闭时终止。 *timeout* 形参为适当的 "select()" 或 "poll()" 调用设置超
   时参数，以秒为单位; 默认值为30秒。 *use_poll* 形参，如果为 True ，
   则表示 "poll()" 应优先使用 "select`（默认为``False`()"）。

   The *map* parameter is a dictionary whose items are the channels to
   watch. As channels are closed they are deleted from their map.  If
   *map* is omitted, a global map is used. Channels (instances of
   "asyncore.dispatcher", "asynchat.async_chat" and subclasses
   thereof) can freely be mixed in the map.

class asyncore.dispatcher

   The "dispatcher" class is a thin wrapper around a low-level socket
   object. To make it more useful, it has a few methods for event-
   handling which are called from the asynchronous loop.   Otherwise,
   it can be treated as a normal non-blocking socket object.

   The firing of low-level events at certain times or in certain
   connection states tells the asynchronous loop that certain higher-
   level events have taken place.  For example, if we have asked for a
   socket to connect to another host, we know that the connection has
   been made when the socket becomes writable for the first time (at
   this point you know that you may write to it with the expectation
   of success).  The implied higher-level events are:

   +------------------------+------------------------------------------+
   | Event                  | 描述                                     |
   |========================|==========================================|
   | "handle_connect()"     | Implied by the first read or write event |
   +------------------------+------------------------------------------+
   | "handle_close()"       | Implied by a read event with no data     |
   |                        | available                                |
   +------------------------+------------------------------------------+
   | "handle_accepted()"    | Implied by a read event on a listening   |
   |                        | socket                                   |
   +------------------------+------------------------------------------+

   During asynchronous processing, each mapped channel's "readable()"
   and "writable()" methods are used to determine whether the
   channel's socket should be added to the list of channels
   "select()"ed or "poll()"ed for read and write events.

   Thus, the set of channel events is larger than the basic socket
   events.  The full set of methods that can be overridden in your
   subclass follows:

   handle_read()

      Called when the asynchronous loop detects that a "read()" call
      on the channel's socket will succeed.

   handle_write()

      Called when the asynchronous loop detects that a writable socket
      can be written.  Often this method will implement the necessary
      buffering for performance.  For example:

         def handle_write(self):
             sent = self.send(self.buffer)
             self.buffer = self.buffer[sent:]

   handle_expt()

      Called when there is out of band (OOB) data for a socket
      connection.  This will almost never happen, as OOB is tenuously
      supported and rarely used.

   handle_connect()

      Called when the active opener's socket actually makes a
      connection.  Might send a "welcome" banner, or initiate a
      protocol negotiation with the remote endpoint, for example.

   handle_close()

      Called when the socket is closed.

   handle_error()

      Called when an exception is raised and not otherwise handled.
      The default version prints a condensed traceback.

   handle_accept()

      Called on listening channels (passive openers) when a connection
      can be established with a new remote endpoint that has issued a
      "connect()" call for the local endpoint. Deprecated in version
      3.2; use "handle_accepted()" instead.

      3.2 版后已移除.

   handle_accepted(sock, addr)

      Called on listening channels (passive openers) when a connection
      has been established with a new remote endpoint that has issued
      a "connect()" call for the local endpoint.  *sock* is a *new*
      socket object usable to send and receive data on the connection,
      and *addr* is the address bound to the socket on the other end
      of the connection.

      3.2 新版功能.

   readable()

      Called each time around the asynchronous loop to determine
      whether a channel's socket should be added to the list on which
      read events can occur.  The default method simply returns
      "True", indicating that by default, all channels will be
      interested in read events.

   writable()

      Called each time around the asynchronous loop to determine
      whether a channel's socket should be added to the list on which
      write events can occur.  The default method simply returns
      "True", indicating that by default, all channels will be
      interested in write events.

   In addition, each channel delegates or extends many of the socket
   methods. Most of these are nearly identical to their socket
   partners.

   create_socket(family=socket.AF_INET, type=socket.SOCK_STREAM)

      This is identical to the creation of a normal socket, and will
      use the same options for creation.  Refer to the "socket"
      documentation for information on creating sockets.

      在 3.3 版更改: *family* and *type* arguments can be omitted.

   connect(address)

      As with the normal socket object, *address* is a tuple with the
      first element the host to connect to, and the second the port
      number.

   send(data)

      Send *data* to the remote end-point of the socket.

   recv(buffer_size)

      Read at most *buffer_size* bytes from the socket's remote end-
      point.  An empty bytes object implies that the channel has been
      closed from the other end.

      Note that "recv()" may raise "BlockingIOError" , even though
      "select.select()" or "select.poll()" has reported the socket
      ready for reading.

   listen(backlog)

      Listen for connections made to the socket.  The *backlog*
      argument specifies the maximum number of queued connections and
      should be at least 1; the maximum value is system-dependent
      (usually 5).

   bind(address)

      Bind the socket to *address*.  The socket must not already be
      bound.  (The format of *address* depends on the address family
      --- refer to the "socket" documentation for more information.)
      To mark the socket as re-usable (setting the "SO_REUSEADDR"
      option), call the "dispatcher" object's "set_reuse_addr()"
      method.

   accept()

      Accept a connection.  The socket must be bound to an address and
      listening for connections.  The return value can be either
      "None" or a pair "(conn, address)" where *conn* is a *new*
      socket object usable to send and receive data on the connection,
      and *address* is the address bound to the socket on the other
      end of the connection. When "None" is returned it means the
      connection didn't take place, in which case the server should
      just ignore this event and keep listening for further incoming
      connections.

   close()

      Close the socket.  All future operations on the socket object
      will fail. The remote end-point will receive no more data (after
      queued data is flushed).  Sockets are automatically closed when
      they are garbage-collected.

class asyncore.dispatcher_with_send

   A "dispatcher" subclass which adds simple buffered output
   capability, useful for simple clients. For more sophisticated usage
   use "asynchat.async_chat".

class asyncore.file_dispatcher

   A file_dispatcher takes a file descriptor or *file object* along
   with an optional map argument and wraps it for use with the
   "poll()" or "loop()" functions.  If provided a file object or
   anything with a "fileno()" method, that method will be called and
   passed to the "file_wrapper" constructor.

   Availability: Unix.

class asyncore.file_wrapper

   A file_wrapper takes an integer file descriptor and calls
   "os.dup()" to duplicate the handle so that the original handle may
   be closed independently of the file_wrapper.  This class implements
   sufficient methods to emulate a socket for use by the
   "file_dispatcher" class.

   Availability: Unix.


asyncore Example basic HTTP client
==================================

Here is a very basic HTTP client that uses the "dispatcher" class to
implement its socket handling:

   import asyncore

   class HTTPClient(asyncore.dispatcher):

       def __init__(self, host, path):
           asyncore.dispatcher.__init__(self)
           self.create_socket()
           self.connect( (host, 80) )
           self.buffer = bytes('GET %s HTTP/1.0\r\nHost: %s\r\n\r\n' %
                               (path, host), 'ascii')

       def handle_connect(self):
           pass

       def handle_close(self):
           self.close()

       def handle_read(self):
           print(self.recv(8192))

       def writable(self):
           return (len(self.buffer) > 0)

       def handle_write(self):
           sent = self.send(self.buffer)
           self.buffer = self.buffer[sent:]


   client = HTTPClient('www.python.org', '/')
   asyncore.loop()


asyncore Example basic echo server
==================================

Here is a basic echo server that uses the "dispatcher" class to accept
connections and dispatches the incoming connections to a handler:

   import asyncore

   class EchoHandler(asyncore.dispatcher_with_send):

       def handle_read(self):
           data = self.recv(8192)
           if data:
               self.send(data)

   class EchoServer(asyncore.dispatcher):

       def __init__(self, host, port):
           asyncore.dispatcher.__init__(self)
           self.create_socket()
           self.set_reuse_addr()
           self.bind((host, port))
           self.listen(5)

       def handle_accepted(self, sock, addr):
           print('Incoming connection from %s' % repr(addr))
           handler = EchoHandler(sock)

   server = EchoServer('localhost', 8080)
   asyncore.loop()
