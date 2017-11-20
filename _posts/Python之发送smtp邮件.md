---
title: Python之发送smtp邮件
date: 2017-11-20 17:09:43
tags:
	- Python
	- 邮件

---



smtp是Simple Mail Transfer Protocol。简单邮件传输协议。

Python的smtplib对smtp协议进行简单的封装。

我的目标是可以发一封邮件到我的QQ邮箱，那应该怎么做呢？

下面代码是从自己的qq邮箱给自己发邮件。

```
#!/usr/bin/python

from email.mime.text import MIMEText
import smtplib

msg = MIMEText('hello, send by python', 'plain', 'utf-8')
from_addr = raw_input("from:")
password = raw_input("password:")
smtp_server = raw_input("smtp server:")#qq的是smtp.qq.com
to_addr = raw_input("to:")


server = smtplib.SMTP_SSL(smtp_server, 465)
server.set_debuglevel(1)
server.login(from_addr, password)
server.sendmail(from_addr, [to_addr], msg.as_string())
server.quit()

```

注意，这段代码做了特别处理了，因为出现了错误了。是qq邮箱处于安全考虑，需要SSL通路，所以SMTP_SSL。还有端口号也换成了465，但是还是不行，因为需要一个授权码。太麻烦。我就先不做了。

我们上面这个邮件并不完善。所以更完备的写法如下。

```
#!/usr/bin/python

from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr

import smtplib
#新增部分
def _format_addr(s):
	name,addr = parseaddr(s)
	return formataddr((Header(name,'utf-8').encoode(),\
	addr.encode('utf-8') if isinstance(addr, unicode) else addr \
	))
	


from_addr = raw_input("from:")
password = raw_input("password:")
smtp_server = raw_input("smtp server:")#qq的是smtp.qq.com
to_addr = raw_input("to:")
#新增部分
msg = MIMEText('hello, send by python', 'plain', 'utf-8')
msg['From'] = _format_addr(u'发邮件的是<%s>' %from_addr)
msg['To'] = _format_addr(u'收邮件的是<%s>' %to_addr)
msg['Subject'] = Header(u'Python邮件','utf-8).encode()

#发送过程一样
server = smtplib.SMTP_SSL(smtp_server, 465)
server.set_debuglevel(1)
server.login(from_addr, password)
server.sendmail(from_addr, [to_addr], msg.as_string())
server.quit()
```

# 如何发送html的邮件

上面构造的都是text纯文本的邮件，要把MIMEText里的plain换成html就可以了。另外hello那个字符串，要用`<html>`这种标签内容替代。

