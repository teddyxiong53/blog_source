---
title: socks5代理之python实现
date: 2019-01-12 14:10:59
tags:
	- 代理
---



知乎到找到一个很好的系列教程。

代码都放在这里。

https://github.com/facert/socket-example



先看简单tcp编程。

server.py

```
from __future__ import print_function
import socket
import threading
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
s.bind(("127.0.0.1", 8888))
s.listen(5)

def handle_tcp(sock, addr):
    print("conn from ", addr)
    sock.send("hello\n")
    while True:
        data = sock.recv(1024)
        if not data:
            break
        sock.send(b"echo [%s]" %data)
    sock.close()

while True:
    sock, addr = s.accept()
    t = threading.Thread(target=handle_tcp, args=(sock,addr))
    t.start()
```

client.py

```
from __future__ import print_function
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("127.0.0.1", 8888))
print(s.recv(1024))

for data in [b'abc']:
    s.send(data)
    print(s.recv(1024))

s.close()
```

再看udp版本的。

server.py

```
from __future__ import print_function
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("127.0.0.1", 8888))
while True:
    data,addr = s.recvfrom(1024)
    print("recv from ", addr)
    s.sendto(b"echo [%s]" % data, addr)
```

client.py

```
from __future__ import print_function
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
for data in [b'abc']:
    s.sendto(data, ("127.0.0.1",8888))
    print(s.recv(1024))
s.close()
```



后面的代码，需要用python3来写。

python2处理不方便。



参考资料

1、由浅入深写代理(4)-socks5-代理

https://www.zhihu.com/topic/20026182/hot

2、系列文章：

https://zhuanlan.zhihu.com/p/28645724

3、socks5协议（rfc1928）

<https://blog.csdn.net/sjailjq/article/details/81637196>