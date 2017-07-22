---
title: shadowsocks之SocketServer
date: 2017-07-22 12:21:15
tags:

	- shadowsocks

---

SocketServer是python提供的实现socket server的模块。利用其API可以快速开发一个socket服务器。总体来说，有4个类：

* TCPServer
* UDPServer
* UnixStreamServer
* UnixDatagramServer

这4个类都是同步的，也就是说，一个请求处理完之后，才能处理下一个请求。当然Python提供了其他的机制来进行并行处理。

# 1. 编写一个Socket Server

要3个基本步骤：

1、编写一个handler类，继承BaseRequestHandler类，重写它的handle方法。

2、针对TCP或者UDP，生成一个server对象。

3、调用server对象的handle_request方法或者serve_forever方法。

server.py

```
#!/usr/bin/python 

import SocketServer
class MyTCPHandler(SocketServer.BaseRequestHandler):
	def handle(self):
		self.data = self.request.recv(1024).strip()
		print "{} wrote".format(self.client_address[0])
		print self.data
		self.request.sendall(self.data.upper())
		
if __name__ == '__main__':
	HOST,PORT = "localhost",9999
	server = SocketServer.TCPServer((HOST, PORT),MyTCPHandler)
	server.serve_forever()
```

写一个client.py

```
#!/usr/bin/python

import socket
import sys

HOST,PORT="localhost",9999
data = " ".join(sys.argv[1])
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
	sock.connect((HOST,PORT))
	sock.sendall(data + "\n")
	received = sock.recv(1024)
finally:
	sock.close()
print "Sent: {}".format(data)
print "received: {}".format(received)
```

开一个shell窗口，执行`./server.py`。另外开一个shell窗口。执行`./client.py hello`。就可以看到效果了。





