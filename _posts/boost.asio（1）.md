---
title: boost.asio（1）
date: 2020-06-02 16:11:08
tags:
	- boost

---

1

下文boost.asio简称为asio。

asio对socket、文件io进行抽象。

提供了同步和异步2套接口：

```
read(stream, buffer, ...);
async_read(stream, buffer, handler);
write(stream, buffer);
async_write(stream, buffer, handler);
```



# 依赖

```
boost.system
boost.regex
boost.datetime
openssl
```



# 同步异步

你在写自己的代码之前，就要决定好是使用同步还是异步方式，中途做改变不是一件容易的事情。

使用同步方式的简单代码：

```
using boost.asio;
io_service service;
ip::tcp::endpoint ep(ip::address::from_string("127.0.0.1"), 2001);
ip::tcp::socket sock(server);
sock.connect(ep);
```

你的程序至少需要一个io_service实例。而且一般只需要一个io_service。

下面是使用同步方式的server的代码。

```
typedef boost::shared_ptr<ip::tcp::socket> socket_ptr;
io_service service;
ip::tcp::endpoint ep(ip::tcp::v4(), 2001);
ip::tcp::acceptor acc(service, ep);

while(true) {
	socket_ptr sock(new ip::tcp::socket(service));
	acc.accept(*sock);
	boost::thread(boost::bind(client_session, sock));
}
void client_session(socket_ptr sock) {
	while(true) {
		char data[512];
		size_t len = sock->read_some(buffer(data));
		if(len > 0) {
			write(*sock, buffer("ok" ,2));
		}
	}
}
```





参考资料

1、Boost.Asio入门

https://mmoaay.gitbooks.io/boost-asio-cpp-network-programming-chinese/content/Chapter1.html