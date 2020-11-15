"email": 示例
*************

以下是一些如何使用 "email" 包来读取、写入和发送简单电子邮件以及更复杂
的MIME邮件的示例。

首先，让我们看看如何创建和发送简单的文本消息（文本内容和地址都可能包含
unicode字符）：

   # Import smtplib for the actual sending function
   import smtplib

   # Import the email modules we'll need
   from email.message import EmailMessage

   # Open the plain text file whose name is in textfile for reading.
   with open(textfile) as fp:
       # Create a text/plain message
       msg = EmailMessage()
       msg.set_content(fp.read())

   # me == the sender's email address
   # you == the recipient's email address
   msg['Subject'] = f'The contents of {textfile}'
   msg['From'] = me
   msg['To'] = you

   # Send the message via our own SMTP server.
   s = smtplib.SMTP('localhost')
   s.send_message(msg)
   s.quit()

解析 **RFC 822** 标题可以通过使用 "parser" 模块中的类来轻松完成：

   # Import the email modules we'll need
   from email.parser import BytesParser, Parser
   from email.policy import default

   # If the e-mail headers are in a file, uncomment these two lines:
   # with open(messagefile, 'rb') as fp:
   #     headers = BytesParser(policy=default).parse(fp)

   #  Or for parsing headers in a string (this is an uncommon operation), use:
   headers = Parser(policy=default).parsestr(
           'From: Foo Bar <user@example.com>\n'
           'To: <someone_else@example.com>\n'
           'Subject: Test message\n'
           '\n'
           'Body would go here\n')

   #  Now the header items can be accessed as a dictionary:
   print('To: {}'.format(headers['to']))
   print('From: {}'.format(headers['from']))
   print('Subject: {}'.format(headers['subject']))

   # You can also access the parts of the addresses:
   print('Recipient username: {}'.format(headers['to'].addresses[0].username))
   print('Sender name: {}'.format(headers['from'].addresses[0].display_name))

以下是如何发送包含可能在目录中的一系列家庭照片的MIME消息示例：

   # Import smtplib for the actual sending function
   import smtplib

   # And imghdr to find the types of our images
   import imghdr

   # Here are the email package modules we'll need
   from email.message import EmailMessage

   # Create the container email message.
   msg = EmailMessage()
   msg['Subject'] = 'Our family reunion'
   # me == the sender's email address
   # family = the list of all recipients' email addresses
   msg['From'] = me
   msg['To'] = ', '.join(family)
   msg.preamble = 'You will not see this in a MIME-aware mail reader.\n'

   # Open the files in binary mode.  Use imghdr to figure out the
   # MIME subtype for each specific image.
   for file in pngfiles:
       with open(file, 'rb') as fp:
           img_data = fp.read()
       msg.add_attachment(img_data, maintype='image',
                                    subtype=imghdr.what(None, img_data))

   # Send the email via our own SMTP server.
   with smtplib.SMTP('localhost') as s:
       s.send_message(msg)

以下是如何将目录的全部内容作为电子邮件消息发送的示例： [1]

   #!/usr/bin/env python3

   """Send the contents of a directory as a MIME message."""

   import os
   import smtplib
   # For guessing MIME type based on file name extension
   import mimetypes

   from argparse import ArgumentParser

   from email.message import EmailMessage
   from email.policy import SMTP


   def main():
       parser = ArgumentParser(description="""\
   Send the contents of a directory as a MIME message.
   Unless the -o option is given, the email is sent by forwarding to your local
   SMTP server, which then does the normal delivery process.  Your local machine
   must be running an SMTP server.
   """)
       parser.add_argument('-d', '--directory',
                           help="""Mail the contents of the specified directory,
                           otherwise use the current directory.  Only the regular
                           files in the directory are sent, and we don't recurse to
                           subdirectories.""")
       parser.add_argument('-o', '--output',
                           metavar='FILE',
                           help="""Print the composed message to FILE instead of
                           sending the message to the SMTP server.""")
       parser.add_argument('-s', '--sender', required=True,
                           help='The value of the From: header (required)')
       parser.add_argument('-r', '--recipient', required=True,
                           action='append', metavar='RECIPIENT',
                           default=[], dest='recipients',
                           help='A To: header value (at least one required)')
       args = parser.parse_args()
       directory = args.directory
       if not directory:
           directory = '.'
       # Create the message
       msg = EmailMessage()
       msg['Subject'] = f'Contents of directory {os.path.abspath(directory)}'
       msg['To'] = ', '.join(args.recipients)
       msg['From'] = args.sender
       msg.preamble = 'You will not see this in a MIME-aware mail reader.\n'

       for filename in os.listdir(directory):
           path = os.path.join(directory, filename)
           if not os.path.isfile(path):
               continue
           # Guess the content type based on the file's extension.  Encoding
           # will be ignored, although we should check for simple things like
           # gzip'd or compressed files.
           ctype, encoding = mimetypes.guess_type(path)
           if ctype is None or encoding is not None:
               # No guess could be made, or the file is encoded (compressed), so
               # use a generic bag-of-bits type.
               ctype = 'application/octet-stream'
           maintype, subtype = ctype.split('/', 1)
           with open(path, 'rb') as fp:
               msg.add_attachment(fp.read(),
                                  maintype=maintype,
                                  subtype=subtype,
                                  filename=filename)
       # Now send or store the message
       if args.output:
           with open(args.output, 'wb') as fp:
               fp.write(msg.as_bytes(policy=SMTP))
       else:
           with smtplib.SMTP('localhost') as s:
               s.send_message(msg)


   if __name__ == '__main__':
       main()

以下是如何将上述MIME消息解压缩到文件目录中的示例：

   #!/usr/bin/env python3

   """Unpack a MIME message into a directory of files."""

   import os
   import email
   import mimetypes

   from email.policy import default

   from argparse import ArgumentParser


   def main():
       parser = ArgumentParser(description="""\
   Unpack a MIME message into a directory of files.
   """)
       parser.add_argument('-d', '--directory', required=True,
                           help="""Unpack the MIME message into the named
                           directory, which will be created if it doesn't already
                           exist.""")
       parser.add_argument('msgfile')
       args = parser.parse_args()

       with open(args.msgfile, 'rb') as fp:
           msg = email.message_from_binary_file(fp, policy=default)

       try:
           os.mkdir(args.directory)
       except FileExistsError:
           pass

       counter = 1
       for part in msg.walk():
           # multipart/* are just containers
           if part.get_content_maintype() == 'multipart':
               continue
           # Applications should really sanitize the given filename so that an
           # email message can't be used to overwrite important files
           filename = part.get_filename()
           if not filename:
               ext = mimetypes.guess_extension(part.get_content_type())
               if not ext:
                   # Use a generic bag-of-bits extension
                   ext = '.bin'
               filename = f'part-{counter:03d}{ext}'
           counter += 1
           with open(os.path.join(args.directory, filename), 'wb') as fp:
               fp.write(part.get_payload(decode=True))


   if __name__ == '__main__':
       main()

以下是如何使用备用纯文本版本创建 HTML 消息的示例。 为了让事情变得更有
趣，我们在 html 部分中包含了一个相关的图像，我们保存了一份我们要发送的
内容到硬盘中，然后发送它。

   #!/usr/bin/env python3

   import smtplib

   from email.message import EmailMessage
   from email.headerregistry import Address
   from email.utils import make_msgid

   # Create the base text message.
   msg = EmailMessage()
   msg['Subject'] = "Ayons asperges pour le déjeuner"
   msg['From'] = Address("Pepé Le Pew", "pepe", "example.com")
   msg['To'] = (Address("Penelope Pussycat", "penelope", "example.com"),
                Address("Fabrette Pussycat", "fabrette", "example.com"))
   msg.set_content("""\
   Salut!

   Cela ressemble à un excellent recipie[1] déjeuner.

   [1] http://www.yummly.com/recipe/Roasted-Asparagus-Epicurious-203718

   --Pepé
   """)

   # Add the html version.  This converts the message into a multipart/alternative
   # container, with the original text message as the first part and the new html
   # message as the second part.
   asparagus_cid = make_msgid()
   msg.add_alternative("""\
   <html>
     <head></head>
     <body>
       <p>Salut!</p>
       <p>Cela ressemble à un excellent
           <a href="http://www.yummly.com/recipe/Roasted-Asparagus-Epicurious-203718">
               recipie
           </a> déjeuner.
       </p>
       <img src="cid:{asparagus_cid}" />
     </body>
   </html>
   """.format(asparagus_cid=asparagus_cid[1:-1]), subtype='html')
   # note that we needed to peel the <> off the msgid for use in the html.

   # Now add the related image to the html part.
   with open("roasted-asparagus.jpg", 'rb') as img:
       msg.get_payload()[1].add_related(img.read(), 'image', 'jpeg',
                                        cid=asparagus_cid)

   # Make a local copy of what we are going to send.
   with open('outgoing.msg', 'wb') as f:
       f.write(bytes(msg))

   # Send the message via local SMTP server.
   with smtplib.SMTP('localhost') as s:
       s.send_message(msg)

如果我们发送最后一个示例中的消息，这是我们可以处理它的一种方法：

   import os
   import sys
   import tempfile
   import mimetypes
   import webbrowser

   # Import the email modules we'll need
   from email import policy
   from email.parser import BytesParser

   # An imaginary module that would make this work and be safe.
   from imaginary import magic_html_parser

   # In a real program you'd get the filename from the arguments.
   with open('outgoing.msg', 'rb') as fp:
       msg = BytesParser(policy=policy.default).parse(fp)

   # Now the header items can be accessed as a dictionary, and any non-ASCII will
   # be converted to unicode:
   print('To:', msg['to'])
   print('From:', msg['from'])
   print('Subject:', msg['subject'])

   # If we want to print a preview of the message content, we can extract whatever
   # the least formatted payload is and print the first three lines.  Of course,
   # if the message has no plain text part printing the first three lines of html
   # is probably useless, but this is just a conceptual example.
   simplest = msg.get_body(preferencelist=('plain', 'html'))
   print()
   print(''.join(simplest.get_content().splitlines(keepends=True)[:3]))

   ans = input("View full message?")
   if ans.lower()[0] == 'n':
       sys.exit()

   # We can extract the richest alternative in order to display it:
   richest = msg.get_body()
   partfiles = {}
   if richest['content-type'].maintype == 'text':
       if richest['content-type'].subtype == 'plain':
           for line in richest.get_content().splitlines():
               print(line)
           sys.exit()
       elif richest['content-type'].subtype == 'html':
           body = richest
       else:
           print("Don't know how to display {}".format(richest.get_content_type()))
           sys.exit()
   elif richest['content-type'].content_type == 'multipart/related':
       body = richest.get_body(preferencelist=('html'))
       for part in richest.iter_attachments():
           fn = part.get_filename()
           if fn:
               extension = os.path.splitext(part.get_filename())[1]
           else:
               extension = mimetypes.guess_extension(part.get_content_type())
           with tempfile.NamedTemporaryFile(suffix=extension, delete=False) as f:
               f.write(part.get_content())
               # again strip the <> to go from email form of cid to html form.
               partfiles[part['content-id'][1:-1]] = f.name
   else:
       print("Don't know how to display {}".format(richest.get_content_type()))
       sys.exit()
   with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
       # The magic_html_parser has to rewrite the href="cid:...." attributes to
       # point to the filenames in partfiles.  It also has to do a safety-sanitize
       # of the html.  It could be written using html.parser.
       f.write(magic_html_parser(body.get_content(), partfiles))
   webbrowser.open(f.name)
   os.remove(f.name)
   for fn in partfiles.values():
       os.remove(fn)

   # Of course, there are lots of email messages that could break this simple
   # minded program, but it will handle the most common ones.

直到输出提示，上面的输出是：

   To: Penelope Pussycat <penelope@example.com>, Fabrette Pussycat <fabrette@example.com>
   From: Pepé Le Pew <pepe@example.com>
   Subject: Ayons asperges pour le déjeuner

   Salut!

   Cela ressemble à un excellent recipie[1] déjeuner.

-[ 脚注 ]-

[1] 感谢 Matthew Dixon Cowles 提供最初的灵感和示例。
