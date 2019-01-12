---
title: python之select用法
date: 2019-01-09 17:59:22
tags:		
	- python
---





从实际看，python里的select，r/w/e，都是socket对象，而不是像C语言里的是fd。



server.py

```
from __future__ import print_function
import socket
import time
import Queue
import select

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
server.setblocking(False)
server.bind(("127.0.0.1", 8080))
server.listen(5)

inputs = [server]
outputs = []
message_queues = {}

while inputs:
    print("waiting for next event")
    readable, writable, exceptional = select.select(inputs, outputs, inputs)

    for s in readable:
        # this means a conn comes
        if s is server:
            connection, client_addr = s.accept()
            print("conn from ", client_addr)
            connection.setblocking(0)
            inputs.append(connection)
            message_queues[connection] = Queue.Queue()
        else:
            # this means data from a client
            data = s.recv(1024)
            if data != "":
                print("recv %s from %s" % (data, s.getpeername()))
                message_queues[s].put(data)
                if s not in outputs:
                    outputs.append(s)
            else:
                print("closing ", client_addr)
                if s in outputs:
                    outputs.remove(s)
                s.close()
                del message_queues[s]

    for s in writable:
        try:
            message_queue = message_queues.get(s)
            send_data = ""
            if message_queue is not None:
                send_data = message_queue.get_nowait()
            else:
                print("client has closed")
        except Queue.Empty:
            print("%s" % (s.getpeername()))
            outputs.remove(s)
        else:
            if message_queue is not None:
                s.send(send_data)
            else:
                print("client closed")

    for s in exceptional:
        print("exception on ", s.getpeername())
        inputs.remove(s)
        if s in outputs:
            outputs.remove(s)
        s.close()
        del message_queues[s]
    time.sleep(1)
```

client.py

```
import socket

messages = ['this is the message', 'It will be sent', 'in pairs']

server_addr = ("127.0.0.1", 8080)

socks = [socket.socket(socket.AF_INET, socket.SOCK_STREAM), socket.socket(socket.AF_INET, socket.SOCK_STREAM)]

print("connect to server %s %s " % (server_addr))

for s in socks:
    s.connect(server_addr)

for index, message in enumerate(messages):
    for s in socks:
        s.send(bytes(message+str(index)).decode("utf-8"))

for s in socks:
    data = s.recv(1024)
    print("%s: received %s" % (s.getsockname(), data))
    if data != "":
        print("closing sock", s.getsockname())
        s.close()
```

运行：

```
hlxiong@hlxiong-VirtualBox:~/work/test/python$ python server.py 
waiting for next event
conn from  ('127.0.0.1', 60682)
waiting for next event
conn from  ('127.0.0.1', 60684)
recv this is the message0It will be sent1in pairs2 from ('127.0.0.1', 60682)
waiting for next event
recv this is the message0It will be sent1in pairs2 from ('127.0.0.1', 60684)
waiting for next event
closing  ('127.0.0.1', 60684)
client has closed
client closed
waiting for next event
Traceback (most recent call last):
  File "server.py", line 18, in <module>
    readable, writable, exceptional = select.select(inputs, outputs, inputs)
  File "/usr/lib/python2.7/socket.py", line 228, in meth
    return getattr(self._sock,name)(*args)
  File "/usr/lib/python2.7/socket.py", line 174, in _dummy
    raise error(EBADF, 'Bad file descriptor')
socket.error: [Errno 9] Bad file descriptor
```

```
hlxiong@hlxiong-VirtualBox:~/work/test/python$ python client.py 
connect to server 127.0.0.1 8080 
('127.0.0.1', 60682): received this is the message0It will be sent1in pairs2
('closing sock', ('127.0.0.1', 60682))
('127.0.0.1', 60684): received this is the message0It will be sent1in pairs2
('closing sock', ('127.0.0.1', 60684))
```



参考资料

1、python select模块详解

https://www.cnblogs.com/huchong/p/8613308.html