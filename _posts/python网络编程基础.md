---
title: python网络编程基础
date: 2016-11-05 16:01:36
tags:
	- python
---
# 1. 简单tcp client
```
import socket
target_host = "www.baidu.com"
target_port = 80

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# the param for connect function is address, address is host+port
client.connect((target_host, target_port))
client.send(r"GET / HTTP/1.1\r\nHost: www.baidu.com\r\n\r\n")
# 4096 is buffer size
response = client.recv(4096)
print response

```
# 2. 简单udp client
```
import socket
target_host = "127.0.0.1"
target_port = 80

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.sendto("aabbcc",(target_host,target_port))
client.recvfrom(4096)
```



