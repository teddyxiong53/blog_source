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

一般都是使用异步的方式，如果没有异步需求，说明场景很简单。使用普通的socket接口就够用了。



使用同步方式的简单代码：

```
using boost.asio;
io_service service;
ip::tcp::endpoint ep(ip::address::from_string("127.0.0.1"), 2001);
ip::tcp::socket sock(server);
sock.connect(ep);
```

**你的程序至少需要一个io_service实例。而且一般只需要一个io_service。**

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

**所有的异步函数都有抛出异常和返回错误码这两种方式的重载。**

当函数抛出错误的时候，它通常抛出boost::system::system_error的错误。

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

**异步函数从来都不抛出异常，因为这样做毫无意义。**

**所以异步函数，必须使用错误码的方式。**



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



# 错误

```
对‘boost::system::generic_category()’未定义的引用
```

需要加上：`-lboost_system`。



# strand

strand的主要作用是在asio中利用多线程进行事件处理的时候，

如果涉及到多线程访问共享资源，

借助于strand类，我们不需要显示的使用线程同步相关的类（比如mutex）

就可以让**多个事件处理函数依次执行。**



简而言之，strand定义了事件处理程序的严格顺序调用。

我们知道，

若多个线程调用了同一个io_context对象的run方法，

那么该对象关联的多个事件处理函数 可能就会被不同的线程同时执行（即并发执行），

若这些事件处理函数访问同一个非线程安全的共享资源时，就可能会产生线程同步问题。

 但是若我们将这些事件处理函数**bind到同一个strand对象上，**

那么asio库保证在上一个事件处理函数处理完成之前是没法执行下一个事件处理函数的（相当于阻止了并发执行）。



看一个简单的例子。





参考资料

https://www.cnblogs.com/upendi/archive/2012/07/13/2590304.html



# 查看boost版本

我现在编译代码不过。所以需要查看一下boost版本。

```
sudo dpkg -S /usr/include/boost/version.hpp
```

得到输出：

```
libboost1.58-dev:amd64: /usr/include/boost/version.hpp
```

官方默认只有1.58版本的。

我的笔记本上是1.72版本的。

就在笔记本上编译。



# 实现echo

异步方式来做。如果用同步的，就直接用socket就好了。

下面的代码是才弄个snapcast里提取出来的。还无法完全正常工作。

问题在于：async_read只有读取到指定长度的数据，才执行回调。这个对于echo这个场景不合适。

```
#include <iostream>
#include <algorithm>
#include <vector>
#include "mylog.h"
#include <array>
#include <cctype>
#include <bitset>
#include <cstddef>

#include <stdio.h>
#include <cstdio>
#include <deque>

#include <boost/asio.hpp>
#include <boost/bind.hpp>
#include <boost/asio/strand.hpp>

using  boost::asio::ip::tcp;
class EchoSession;

using acceptor_ptr =  std::unique_ptr<tcp::acceptor>;
using session_ptr = std::shared_ptr<EchoSession>;


class MessageReceiver
{
public:
    virtual void onMessageReceived(
        EchoSession *session,
        char *buffer
    ) = 0;
    virtual void onDisconnect(EchoSession *session) = 0;
};

class EchoSession: public std::enable_shared_from_this<EchoSession>
{
public:
    EchoSession(boost::asio::io_context& ioc, MessageReceiver* messageReceiver,tcp::socket&& socket)
    : m_strand(ioc),
      m_socket(std::move(socket)),
      m_bufferSize(2),
      m_messageReceiver(messageReceiver)
    {
        m_buffer.resize(m_bufferSize);
    }
    void start();
    void read_next();
    void sendAsync(char *msg);
    void send_next();
private:
    // boost::asio::io_context& m_ioContext;
    //只需要用strand
    boost::asio::io_context::strand m_strand;
    tcp::socket m_socket;
    std::vector<char> m_buffer;
    size_t m_bufferSize;
    std::deque<char*> m_messages;
    MessageReceiver* m_messageReceiver;

};
void EchoSession::sendAsync(char *msg)
{
    m_strand.post(
        [this, msg]() {
            m_messages.push_back(msg);
            send_next();
        }
    );
}
void EchoSession::send_next()
{
    std::shared_ptr<EchoSession> self;
    self = shared_from_this();
    char *msg = m_messages.front();
    boost::asio::async_write(
        m_socket,
        boost::asio::buffer(m_buffer, m_bufferSize),
        boost::asio::bind_executor(
            m_strand,
            [this, self](boost::system::error_code ec, std::size_t length) {
                m_messages.pop_front();
                if(!ec) {
                    myloge("write error, %s", ec.message().c_str());
                    m_messageReceiver->onDisconnect(this);
                }
                if(!m_messages.empty()) {
                    send_next();
                }
            }
        )

    );
}

void EchoSession::read_next()
{
    std::shared_ptr<EchoSession> self;
    self = shared_from_this();
    boost::asio::async_read(
        m_socket,
        boost::asio::buffer(m_buffer, m_bufferSize),
        boost::asio::bind_executor(
            m_strand,
            [this, self](boost::system::error_code ec, std::size_t length) mutable {
                if(ec) {
                    mylogd("read %d data fail, %s", length, ec.message().c_str());
                    return;
                }
                mylogd("recv:%s", m_buffer.data());
                //发送数据
                //继续调用async_read
                boost::asio::bind_executor(
                    m_strand,
                    [this, self](boost::system::error_code ec, std::size_t length) mutable {
                        if(ec) {
                            mylogd("read %d data fail, %s", length, ec.message().c_str());
                            return;
                        }
                        read_next();
                    }

                );
            }
        )
    );
}
void EchoSession::start()
{
    read_next();
}


class EchoServer: public MessageReceiver
{
public:
    EchoServer(boost::asio::io_context& io_context)
    : m_ioContext(io_context)
    {

    }
    void start()
    {
        m_acceptor.reset(new tcp::acceptor(m_ioContext,
            tcp::endpoint(
                boost::asio::ip::address::from_string("0.0.0.0"),
                2020
            )
        ));
        startAccept();
    }
    virtual void onMessageReceived(
        EchoSession *session,
        char *buffer
    ) override;
    virtual void onDisconnect(EchoSession *session) override;
private:
    void startAccept();
    void handleAccept(tcp::socket socket);
    void cleanup();
    session_ptr getSession(EchoSession *s);
    boost::asio::io_context& m_ioContext;
    acceptor_ptr m_acceptor;
    std::mutex m_sessionMutex;
    std::vector<std::weak_ptr<EchoSession>> m_sessions;

};

session_ptr EchoServer::getSession(EchoSession *s)
{
    std::lock_guard<std::mutex> lock(m_sessionMutex);
    for(auto session: m_sessions) {
        if(auto ss = session.lock()) {
            if(ss.get() == s) {
                return ss;
            }
        }

    }
    return nullptr;
}

void EchoServer::onMessageReceived(
        EchoSession *session,
        char *buffer
    )
{
    session->sendAsync(buffer);

}
/*
    移除对应的session。
*/
void EchoServer::onDisconnect(EchoSession *session)
{
    session_ptr s = getSession(session);
    if(s == nullptr) {
        mylogd("session is null");
        return;
    }
    m_sessions.erase(
        std::remove_if(
            m_sessions.begin(),
            m_sessions.end(),
            [session](std::weak_ptr<EchoSession> es) {
                auto s = es.lock();
                return s.get() == session;
            }
        ),
        m_sessions.end()
    );
    cleanup();

}
void EchoServer::cleanup()
{
    auto new_end = std::remove_if(
        m_sessions.begin(),
        m_sessions.end(),
        [](std::weak_ptr<EchoSession> session) {
            return session.expired();
        }
    );
    auto count = std::distance(new_end, m_sessions.end());
    if(count > 0) {
        mylogd("removing %d session, total:%d", count, m_sessions.size());
        m_sessions.erase(new_end, m_sessions.end());
    }
}
void EchoServer::handleAccept(tcp::socket socket)
{
    struct timeval tv;
    tv.tv_sec = 5;
    tv.tv_usec = 0;
    setsockopt(socket.native_handle(), SOL_SOCKET, SO_RCVTIMEO, &tv, sizeof(tv));
    setsockopt(socket.native_handle(), SOL_SOCKET, SO_SNDTIMEO, &tv, sizeof(tv));
    socket.set_option(tcp::no_delay(true));
    mylogd("accept connection from:%s", socket.remote_endpoint().address().to_string().c_str());
    std::shared_ptr<EchoSession> session = std::make_shared<EchoSession>(m_ioContext, this, std::move(socket));
    session->start();
    std::lock_guard<std::mutex> lock(m_sessionMutex);
    m_sessions.emplace_back(session);
    cleanup();
    startAccept();//handleAccept和startAccept互相递归调用
}

void EchoServer::startAccept()
{
    auto accept_handler = [this](boost::system::error_code ec, tcp::socket socket) {
        if(!ec) {
            handleAccept(std::move(socket));
        } else {
            myloge("accept fail %s", ec.message().c_str());
        }
    };
    m_acceptor->async_accept(accept_handler);
}


int main(int argc, char const *argv[])
{
    boost::asio::io_context io_context;
    std::unique_ptr<EchoServer> server(new EchoServer(io_context));
    server->start();
    io_context.run();//这里阻塞
    return 0;
}

```



这个只有读取到指定长度的内容了，函数才执行回调。

```
boost::asio::async_read
```

asio::async_read通常用户读取指定长度的数据，读完或出错才返回(会超指定buffer的长度，

不信，你可有用ssl的方式写一个https的通信，用from-urlencoded方式传递下试试)

建议使用async_read_some函数，一定不会出错，出错说明代码问题

boost::asio::buffer里面的参数填string对象和vector<char>对象，有可能发生内存越界(使用async_read方法)



# 异步写测试例子

## 定时器

```
#include <boost/asio.hpp>
#include <iostream>

void handler(const boost::system::error_code &ec)
{
    std::cout << "time out\n";
}

int main(int argc, char const *argv[])
{
    boost::asio::io_context ioc;
    boost::asio::deadline_timer timer(ioc, boost::posix_time::seconds(1));
    timer.async_wait(handler);
    ioc.run();
    std::cout << "end of code\n";
    return 0;
}
```

在 main() 的最后，再次在唯一的 I/O 服务之上调用了 run() 方法。 

如前所述，这个函数将阻塞执行，

把控制权交给操作系统以接管异步处理。 

在操作系统的帮助下，handler1() 函数会在五秒后被调用，而 handler2() 函数则在十秒后被调用。  

乍一看，你可能会觉得有些奇怪，

为什么异步处理还要调用阻塞式的 run() 方法。

 然而，由于应用程序必须防止被中止执行，所以这样做实际上不会有任何问题。

 如果 run() 不是阻塞的，main() 就会结束从而中止该应用程序。 

如果应用程序不应被阻塞，那么就应该在一个新的线程内部调用 run()，它自然就会仅仅阻塞那个线程。



Boost.Asio 提供了多个 I/O 对象以开发网络应用。 

以下例子使用了 boost::asio::ip::tcp::socket 类来建立与中另一台PC的连接，

并下载 'Highscore' 主页；

就象一个浏览器在指向 www.highscore.de 时所要做的。

## tcp client读取网页

```
#include <boost/asio.hpp>
#include <iostream>
#include <boost/array.hpp>



boost::asio::io_context ioc;
boost::asio::ip::tcp::resolver resolver(ioc);
boost::asio::ip::tcp::socket sock(ioc);
boost::array<char, 4096> buffer;

void read_handler(const boost::system::error_code& ec, std::size_t bytes_transferred)
{
    if(!ec) {
        std::cout << std::string(buffer.data(), bytes_transferred);
        sock.async_read_some(boost::asio::buffer(buffer), read_handler);
    }
}

void connect_handler(const boost::system::error_code &ec)
{
    if(!ec) {
        boost::asio::write(sock, boost::asio::buffer("GET / HTTP 1.1\r\nHost: www.baidu.com\r\n\r\n"));
        sock.async_read_some(boost::asio::buffer(buffer), read_handler);
    }
}

void resolve_handler(const boost::system::error_code &ec,
    boost::asio::ip::tcp::resolver::iterator it
)
{
    if(!ec) {
        sock.async_connect(*it, connect_handler);
    }
}
int main(int argc, char const *argv[])
{
    boost::asio::ip::tcp::resolver::query query("www.baidu.com","80");
    resolver.async_resolve(query, resolve_handler);
    ioc.run();
    return 0;
}
```

这个程序最明显的部分是三个句柄的使用：

connect_handler() 和 read_handler() 函数会分别在连接被建立后以及接收到数据后被调用。

 那么为什么需要 resolve_handler() 函数呢？

互联网使用了所谓的IP地址来标识每台PC。

 IP地址实际上只是一长串数字，难以记住。 

而记住象 www.highscore.de 这样的名字就容易得多。 

为了在互联网上使用类似的名字，需要通过一个叫作[域名解析](https://cloud.tencent.com/product/cns?from=10680)的过程将它们翻译成相应的IP地址。

 这个过程由所谓的域名解析器来完成，对应的 I/O 对象是：boost::asio::ip::tcp::resolver。 



域名解析也是一个需要连接到互联网的过程。

 有些专门的PC，被称为DNS服务器，

其作用就象是电话本，它知晓哪个IP地址被赋给了哪台PC。 

由于这个过程本身的透明的，只要明白其背后的概念以及为何需要 boost::asio::ip::tcp::resolver I/O 对象就可以了。 

由于域名解析不是发生在本地的，所以它也被实现为一个异步操作。

 一旦域名解析成功或被某个错误中断，resolve_handler() 函数就会被调用。

## 简单的tcp server

```
#include <boost/asio.hpp>
#include <iostream>
#include <boost/array.hpp>


boost::asio::io_context ioc;
boost::asio::ip::tcp::endpoint endpoint(boost::asio::ip::tcp::v4(), 8082);
boost::asio::ip::tcp::acceptor acceptor(ioc, endpoint);
boost::asio::ip::tcp::socket sock(ioc);

void write_handler(const boost::system::error_code &ec, std::size_t sz)
{
    std::cout << "write finish\n";
}
void accept_handler(const boost::system::error_code &ec)
{
    if(!ec) {
        boost::asio::async_write(sock, boost::asio::buffer("hello asio"), write_handler);
    }
}
int main(int argc, char const *argv[])
{
    acceptor.listen();
    acceptor.async_accept(sock, accept_handler);
    ioc.run();
    return 0;
}
```





https://cloud.tencent.com/developer/article/1056970



# 参考资料

1、Boost.Asio入门

https://mmoaay.gitbooks.io/boost-asio-cpp-network-programming-chinese/content/Chapter1.html

2、asio::io_service被废弃的问题

https://blog.csdn.net/liuqun69/article/details/93009475

3、C++boost之asio strand

https://blog.csdn.net/u010005508/article/details/82819000

4、c++ boost::asio::async_read与Socket的async_read_some的区别

https://blog.csdn.net/qq_33048069/article/details/105531494