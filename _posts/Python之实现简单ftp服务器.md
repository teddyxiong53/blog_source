---
title: Python之实现简单ftp服务器
date: 2018-07-12 22:06:41
tags:
	- Python

---



#ftp的主动模式和被动模式

##主动模式

过程

1、client以端口N对server的21号端口发起连接。

2、client监听N+1号端口。

3、server用20号端口对client的N+1端口进行连接。

优点：

1、服务器配置简单。利于服务器的安全管理。

2、服务器只需要开放21号端口。

缺点：

1、如果client在内网环境里，那么就可能server无法连接到client。

## 被动模式

过程：

1、client以随机端口连接到server的21号端口。

2、服务器开启一个非特权端口为被动端口，并返回给客户端。

3、客户端连接服务器返回的端口。

优点：

1、对client没有什么特别要求。

缺点：

1、server端就复杂一些，不利于安全。



安装依赖库

pip install pyftpdlib



# ftp_server.py

```
#coding: utf-8
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

# 实例化虚拟用户，这是FTP验证首要条件
authorizer = DummyAuthorizer()
# 添加有名用户
authorizer.add_user('admin', 'admin', './' , perm='elradfmw')
#添加匿名用户
authorizer.add_anonymous('./everyone')

handler = FTPHandler
handler.authorizer =authorizer

server = FTPServer(('0.0.0.0', 2121), handler)

server.serve_forever()
```

运行这个脚本。

然后在浏览器里输入：ftp://127.0.0.1:2121/

就可以访问到了。默认没有要求用户名和密码。所以看到的是everyone这个目录下的东西。

先不管。我们可以用一个ftp客户端工具来输入用户名和密码进行访问。

默认的server是主动式的。

如何修改为被动模式的呢？

只需要加上这一行就好了。

```
handler.passive_ports = range(8000,8100)
```



权限字符说明

读权限

```
e：改变文件目录
l：列出文件。
r：从服务器接受文件

```

写权限

```
a：文件上传。
d：删除文件。
f：文件重命名。
m：创建文件。
w：写权限。
M：文件传输模式。
```



# 参考资料

1、python实现FTP服务器服务的方法

https://www.jb51.net/article/110901.htm