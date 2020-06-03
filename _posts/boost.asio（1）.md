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

异步方式的代码：

```
using boost::asio;
typedef boost::shared_ptr<ip::tcp::socket> socket_ptr;
io_service service;
ip::tcp::endpoint ep(ip::tcp::v4(), 2001);
ip::tcp::acceptor acc(service, ep);
//上面部分跟跟同步的一样。

socket_ptr sock(new ip::tcp::socket(service));
start_accept(sock);
service.run();//这个相当于主循环。

void start_accept(socket_ptr sock) {
	acc.async_accept(*sock, boost::bind(handle_accept, sock, _1));
}
void handle_accept(socket_ptr sock, const boost::system::error_code err) {
	if(err) {
		return;
	}
	socket_ptr sock(new ip::tcp::socket(service));
	start_accept(sock);
}
```

# 异常处理和错误码

asio同时支持错误码和异步处理。

所有的异步函数都有抛出异常和返回错误码这两种方式的重载。

当函数抛出错误的食盒，它通常抛出boost::system::system_error的错误。

```
try {
	sock.connect(ep);
} catch(boost::system::system_error e) {
	std::cout << e.code() << "\n";
}
```

等价于

```
boost::system::system_error err;
sock.connect(ep, err);
if(err) {
	std::cout << err << "\n";
}
```

异步函数从来都不抛出异常，因为这样做毫无意义。

所以异步函数，必须使用错误码的方式。



# asio的线程



# asio的namespace

```
boost::asio
	这个是核心类和函数空间。
	重要的类是：io_service和streambuf。
boost::asio::ip
	这个是网络通信部分空间。
	重要的类：address, endpoint, tcp, udp, icmp
	重要的函数：connect, async_connect
	
boost::asio::error
	错误码。
boost::asio::ssl
	ssl相关。
boost::asio::local
	unix的本地socket
boost::asio::windows
	windows特有部分。
```



# socket成员方法

## 连接相关

```
assign(protocol, socket)
open(protocol)
bind(endpoint)
connect(endpoint)
async_connect(endpoint)
is_open()
close()
shutdown(type)
cancel()//马上取消该socket的所有异步操作。返回error::operation_aborted错误。
```

举例如下：

```
ip::tcp::endpoint ep(ip::address::from_string("127.0.0.1"), 80);
ip::tcp::socket sock(service);
sock.open(ip::tcp::v4());
sock.connect(ep);
sock.write_some(buffer("GET /index.html\r\n"));
char buff[1024];
sock.read_some(buffer(buff, 1024));
sock.shutdown(ip::tcp::socket::shutdown_receive);
sock.close();
```

## 读写函数

对于异步函数，handler函数句柄的格式都是一样的，如下：

```
void handler(const boost::system::error_code& e, size_t bytes);
```

异步函数：

```
async_receive(buffer, [flags,] handler)
async_read_some(buffer, handler)//这2个函数作用一样。
async_receive_from(buffer, endpoint[,flags], handler);//相当于socket的recvfrom

async_send(buffer[,flags], handler)
async_write_some(buffer, handler)
async_send_to(buffer, endpoint, handler)
```

同步函数：

```
receive(buffer[,flags])
read_some(buffer)
receive_from(buffer, endpoint[,flags])

send(buffer[,flags])
write_some(buffer)
send_to(buffer, endpoint[,flags])

avaiable();//这个表示可读的字节数。
```

## 其他函数

```
local_endpoint
remote_endpoint
native_handle() //返回原始socket结构体指针
non_blocking()//如果是非阻塞，返回true

```

## 注意

socket不能进行拷贝构造。

# socket buffer

当从一个socket读写内容时，你需要一个buffer。

用来保存数据。

缓冲区的有效时间必须比io操作的时间要长。

对于同步操作，这个很简单。

```
{
	char buff[512];
	sock.receive(buffer(buff));
	strcpy(buff, "ok\n");
	sock.send(buffer(buff));
}
```

下面的异步操作，就是一个错误示范。

```
void on_read(const boost::system::error_code& err, std::size_t bytes)
{
//...
}
void func() {
	char buf[512];
	sock.async_receive(buffer(buff), on_read);
}
```

buff对应的内存在on_read里，已经失效了。

解决这个问题的办法：

```
1、使用全局buffer。
	这个非常不好。
2、使用heap。
	使用智能指针。
3、使用集合处理。
```



# io_context

新版 ASIO 必须以 `asio::io_context` 替换 `asio::io_service`



参考资料

1、Boost.Asio入门

https://mmoaay.gitbooks.io/boost-asio-cpp-network-programming-chinese/content/Chapter1.html

2、asio::io_service被废弃的问题

https://blog.csdn.net/liuqun69/article/details/93009475