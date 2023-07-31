---
title: jsonrpc（1）
date: 2020-04-29 13:49:08
tags:
	- json

---

--

看snapcast里用了jsonrpc来做控制。

rpc我还没有怎么使用过。了解一下。

什么是rpc？有哪些常见的方案？

rpc是Remote Procedure Call，远程过程调用。

简单说，就是一台设备上通过传递参数的方式，调用另外一台设备上的函数，并且把结果返回给调用的机器。

rpc是一个请求响应模型。

使用起来，感觉跟使用本地的一个函数一样。

常见的rpc框架有：

```
dubbo
	阿里巴巴开源的，java写的。
	可以跟spring框架集成。
motan
	新浪微博开源的，java的。
rpcx
	go语言的。跟dubbo差不多。
thrift
	apache的，跨语言的高性能框架。
jsonrpc
	无状态，轻量级。
```

# 发展历史

JSON-RPC的发展历史可以追溯到2005年，以下是其主要发展阶段和里程碑：

1. 提出阶段：JSON-RPC最初由Doug Crockford在2005年提出，作为一种轻量级的远程过程调用（RPC）协议。Crockford是JSON数据格式的创造者之一，他希望用JSON来替代更为复杂的RPC协议，使远程调用更简单、易用。

2. 规范发布：随后，JSON-RPC的第一个正式规范（Version 1.0）于2005年发布。这个规范定义了JSON-RPC消息的结构和基本通信规则，使得不同平台和编程语言之间可以进行简单的RPC通信。

3. JSON-RPC 2.0：在2010年，随着JSON-RPC的普及和广泛应用，一个新的版本JSON-RPC 2.0被提出。JSON-RPC 2.0修复了一些1.0版本的不足，对协议进行了优化和简化，也更加符合JSON的设计理念。JSON-RPC 2.0成为目前应用更广泛的版本，大多数实现都遵循该规范。

4. 应用拓展：随着Web服务和分布式系统的发展，JSON-RPC逐渐成为一种重要的通信协议。许多开发者和组织开始在其应用中广泛使用JSON-RPC作为通信协议，使得不同系统和平台之间可以方便地进行远程调用和数据交换。

5. JSON-RPC over HTTP：由于HTTP是广泛支持的协议，JSON-RPC也被广泛用于Web服务。许多系统将JSON-RPC的消息封装在HTTP请求中，通过HTTP协议进行传输，使得JSON-RPC更容易与Web应用集成。

6. 扩展功能：随着应用场景的多样化，一些变种和扩展功能出现，如支持批量请求、通知（不需要响应的请求）、异步调用等。

总体来说，JSON-RPC作为一种简单、轻量且跨语言的通信协议，经过多年的发展，已成为许多应用中的常用协议之一。它在Web服务、分布式系统、API调用等场景中广泛应用，并为不同系统间的通信提供了一种方便的解决方案。

# jsonrpc通知举例

JSON-RPC通知是一种不需要获得响应的远程调用方式，即客户端向服务器发送请求，但不期望获得任何响应。通知的主要特点是客户端无需等待服务器的回复，适用于那些只需要发送消息给服务器而无需获取结果的场景。

下面是一个JSON-RPC通知的示例：

客户端发送的JSON-RPC通知请求：
```json
{
  "jsonrpc": "2.0",
  "method": "notify",
  "params": {
    "message": "Hello from the client!"
  }
}
```

在这个例子中，客户端发送了一个通知请求，调用了名为 "notify" 的方法，将消息 "Hello from the client!" 作为参数传递给服务器。然而，客户端不期望服务器返回任何响应。

服务器收到通知请求后，执行 "notify" 方法的相应逻辑，但不需要返回结果。

需要注意的是，JSON-RPC通知不包含 "id" 字段，这是与普通请求的主要区别。 "id" 字段用于标识请求与响应的对应关系，而通知不需要响应，因此没有 "id" 字段。

JSON-RPC通知适用于以下场景：

1. 无需返回结果：当客户端只需要向服务器发送消息，而不需要等待服务器的响应时，可以使用通知。

2. 异步通信：通知允许客户端在后台异步地向服务器发送消息，而不会阻塞或等待响应。

3. 无顺序要求：通知请求是无序的，因此客户端可以同时发送多个通知，而不需要等待前一个通知的完成。

需要注意的是，由于JSON-RPC通知不要求服务器返回响应，因此服务器应该在处理通知时，不进行任何需要返回结果的操作。通知通常用于单向通信和简单的数据传输，而非用于请求-响应的复杂场景。



# 让jsonrpc server主动给所有client发送通知

在JSON-RPC中，通常是客户端向服务器发送请求，然后服务器响应这些请求。然而，如果你希望JSON-RPC服务器主动向所有客户端发送通知，你需要使用一些额外的机制来实现这个功能。

一种常见的方法是，服务器与每个客户端建立长连接（例如WebSocket连接），然后在服务器端有需要通知客户端的事件发生时，主动发送通知消息给所有连接的客户端。这样，服务器就可以在任何时候向所有客户端推送消息。

以下是一个示意图：

```
      +--------+                  +--------+
      | Client |                  | Client |
      +--------+                  +--------+
         |    \                     /    |
         |     \                   /     |
   WebSocket   \                 /  WebSocket
       |        \               /       |
       |         \             /        |
      +-----------+          +-----------+
      |   Server  |    ----> |   Server  |
      +-----------+          +-----------+
```

在这种情况下，服务器需要维护所有连接的客户端列表，并在需要时向列表中的所有客户端发送通知。

实现这样的功能可能涉及到服务器端和客户端的WebSocket代码，以及连接管理和消息处理的逻辑。具体实现方式会因所使用的编程语言和框架而有所不同。

需要注意的是，服务器向客户端主动发送通知需要维护客户端连接的状态，这可能会增加服务器的负担。同时，客户端也必须保持长连接以接收服务器的通知，这对于一些应用来说可能并不是最佳选择。

因此，在实现JSON-RPC服务器主动发送通知之前，请仔细考虑你的应用需求和技术栈，并确保服务器和客户端之间的连接管理和消息处理逻辑是有效和高效的。

# 官方文档

规范文档是这个：

https://wiki.geekdream.com/Specification/json-rpc_2.0.html

总结一下：

如果不包含该id成员则被认定为是一个通知。

服务端必须不回复一个通知，包含那些批量请求中的。

回复中必须包含id，且跟请求的id值要一样。



# 一个rpc框架需要实现的功能

因为rpc在使用形式上跟调用本地的函数一样，所以需要解决这3个问题

1、寻址。就是告诉服务端调用的是哪个函数，可以用字符串或者一个id。

2、序列化和反序列化。就是参数要通过网络传递出去，再解析出来使用。

3、网络传输。可以用socket、http、http2.



# http

http本身也可以看做是rpc的一种具体形式。

http请求也可以看做是客户端发送一个信号到服务端，服务端执行某个函数，然后返回一些结果给客户端。

http请求非常常见。

如果我们想要开放自己的机器给其他人使用。那么使用http api是非常合适的。

缺点是通用性不够。

## http和rpc的异同

相同点：

1、http请求和rpc都具有请求和响应。二者的基本过程是一样的。

不同点：

1、http请求是围绕资源，而rpc是围绕一个动作。



# json-rpc

jsonrpc是一个无状态且轻量级的rpc协议。

bitcoin也用到了jsonrpc。

jsonrpc有1.0和2.0 这2个版本。二者有差别。我们只看2.0的。

在2.0里，一个rpc请求需要包含一下4个字段：

```
1、jsonrpc：指定jsonrpc版本。值固定为2.0
2、id。
3、method。要调用的函数
4、params。函数的参数。没有则为[]。可以是object或者array。
```

一个rpc响应，要有下面的字段。

```
1、jsonrpc。版本号，固定为2.0
2、id。
3、result。成功时。
4、error。失败时。
	error有3个字段：
	1、code。整数。
	2、message。
	3、data。附加信息。
```



使用

Parser的parse函数里，就进行了回调函数的调用。只有Notification和Request这2个会调用回调，因为只有他们有回调函数。

parse函数的本质是：把json字符串，构造成对应的Entity类对象。

```
inline entity_ptr Parser::do_parse_json(const Json& json)
{
    try
    {
        if (is_request(json))
            return std::make_shared<Request>(json);
        if (is_notification(json))
            return std::make_shared<Notification>(json);
        if (is_response(json))
            return std::make_shared<Response>(json);
        if (is_batch(json))
            return std::make_shared<Batch>(json);
    }
```



# jsonrpc和restful api

两者没有高下之分，无非是一种约定俗成的标准。习惯用RPC就用RPC，能理解REST就用REST。

JSON-RPC比较符合直观，格式也相对宽松；

REST最近正流行，有自己的一套设计规范。



REST是一种设计风格，它的很多思维方式与RPC是完全冲突的。

**RPC的思想是把本地函数映射到API，**

**也就是说一个API对应的是一个function，**

我本地有一个getAllUsers，远程也能通过某种约定的协议来调用这个getAllUsers。

**至于这个协议是Socket、是HTTP还是别的什么并不重要；**



RPC中的主体都是动作，是个动词，表示我要做什么。

**而REST则不然，它的URL主体是资源，是个名词。**

而且也仅支持HTTP协议，规定了使用HTTP Method表达本次要做的动作，类型一般也不超过那四五种。

这些动作表达了对资源仅有的几种转化方式。

这种设计思路是反程序员直觉的，因为在本地业务代码中仍然是一个个的函数，是动作，但表现在接口形式上则完全是资源的形式。



当然，API怎么写是开发者的自由。但如果一个API在url里放一堆动词、资源设计混乱、各种乱用HTTP Method和Status Code，还自称RESTful API的话，那就像你养了一条狗，还管它叫猫一样。

这种混搭产物，不如叫它REFU吧。

（Remove Extension From Url：从url里去掉文件扩展名）



简单来说：不管哪个“好”还是不“好”，RESTful API在很多实际项目中并不使用。

因此真的做了项目，你可能会发现只能用HTTP+JSON来定义接口，无法严格遵守REST风格。

为什么说不实际呢？因为这个风格太理想化了



# 各种语言的实现版本

## C语言

https://github.com/hmng/jsonrpc-c

依赖了libev和cjson。

这个是基于autotools来进行编译的。

代码少。可以参考一下。

编译方法：

```
autorefconf -i
./configure
make
```

cjson的文件是直接放进来的。因为就2个。而libev是靠依赖的。

这个怎么进行测试呢？

这里是一个python写的命令行工具。

https://github.com/joehillen/jsonrpcake

用pip可以安装。安装后试了，连不上去。

想了一下，可以用netcat来做。

这里有例子。

https://github.com/paritytech/jsonrpc/issues/120

运行有效果：

```
amlogic@amlogic-BAD-INDEX:~$ netcat localhost 1234 -
{"id":1,"jsonrpc":"2.0","method":"sayHello"}
{
        "result":       "Hello!",
        "id":   1
}
```

现在可以分析一下代码了。

流程用思维导图画再这里：

https://naotu.baidu.com/file/1ff3a94bb69723da429f7fa34eacab48

做的都是最基础的处理。够用。健壮性肯定还是不太够的。

连接的buffer，默认分配了1500字节，如果发现接近了这个数字，那么就自动分配多一倍的空间。

## 另一个C语言

https://gitee.com/hy0kl/event-json-rpc/tree/master



# 使用jsonrpc作为主要通信手段的软件有哪些？

想要找一个例子，大量使用jsonrpc作为通信手段的大型软件，看看jsonrpc可以应用到什么程度。

好像没有找到太多。我之前了解这个就是snapcast，那么看起来snapcast反而是用得比较多的。

https://json-rpc.info/ 

这个官网倒是列举了使用json rpc的例子。



https://blog.csdn.net/weixin_29662245/article/details/114959400



# RPC机制

参考资料

https://blog.csdn.net/qq_36183935/article/details/80550457



# 以太坊使用的jsonrpc

https://blog.csdn.net/cljdsc/article/details/110468066

# 自己用jsonrpc做本地进程通信的实践

网上找不到太多的这种用法。

我只是直观上觉得这种方式简单容易理解。

比起dbus要轻量很多，看看能不能在嵌入式Linux里作为一个基础的进程通信机制来使用。

会有哪些问题？

性能可能是一个问题。但是我的只是需要传递一些简单的控制信息。

dbus的二进制方式实在是太繁琐了。

为了做最小的实现。

这个是我之前把jsonrpcpp的自己写了一遍的。c++版本。

https://github.com/teddyxiong53/myjsonrpcpp

现在是打算弄一个C语言的版本。

demo就弄server、client1、client2

实现client到server的get/set。

server的主动notify。

这个就有个基本的雏形了。

https://github.com/hmng/jsonrpc-c

基于这个来改。

我fork一个过来。

configure不过。

```
--with-libev[=PATH]     Search for libev in PATH/include and PATH/lib
```

因为我当前使用的服务器，我没有root权限。不能自由安装软件。

所以自己编译一个libev的库。

libev和libevent不是一个东西。

代码在这里：

https://github.com/enki/libev

编译安装libev

```
./configure --prefix=$HOME
make && make install
```

这样是安装到了我的home目录。

lib目录：

```
.
├── libev.a
├── libev.la
├── libev.so -> libev.so.4.0.0
├── libev.so.4 -> libev.so.4.0.0
└── libev.so.4.0.0

```

include目录

```
.
├── event.h
├── ev++.h
└── ev.h
```

share目录

```
.
└── man
    └── man3
        └── ev.3
```

现在再编译jsonrpc-c的。

```
./configure --with-libev=$HOME
```

编译还是报错。需要加上：

```
./configure --with-libev=$HOME LDFLAGS="-lm"
```

client到server的好理解。

server到client的通路有吗？

是不是一切通信都要由client端发起？

server能不能进行广播？

还是仔细看看snapcast的这个协议设计。

https://github.com/badaix/snapcast/blob/master/doc/json_rpc_api/control.md

理解了一下，server还是不会主动产生状态变化的。

有notify，也是其中一个client变化了。

然后server再主动给所有的client发送这个信息。

snapcast的server端会收到这么三种消息：

```
1、以Client.开头的。
2、以Group.开头的。
3、以Server.开头的。
4、以Stream.开头的。

```

现在最关键的一点就是，server怎么给所有的client发广播。

这里有个讨论。

https://groups.google.com/g/json-rpc/c/2WyxWKSiz8o

那么是不是在snapcast里，snapserver同时作为了jsonrpc的server和client。

同理，snapclient也是同时作为了jsonrpc的server和client。

取决于你如何实现server和client。

或者是说，我需要的，是我的服务器和客户端，其实本质上都是json rpc 的server。

不带id的，就是通知。

那么port是怎么定义呢？

我想清楚了。

就是当前的server实现需要修改一下，在收到没有id的消息时，把所有的client遍历发送一遍数据，就相当于通知了。

当前是没有实现这个的。

可以加上这个特性。



想到这里，我觉得jsonrpc的自由度还是不够高。

是不是可以在嵌入式Linux里，用mqtt broker来做mqtt的系统消息总线呢？

而mqtt消息体内部，使用json格式来组织。

另外开一篇文章《mqtt作为系统消息总线的思考》来梳理这个想法。



## server主动Notification的思考

这个确实是没有。因为是基于请求应答的模型。

2022年12月3日09:02:50

想明白了jsonrpc的通知怎么做了，

进程A作为server，内部同时运行jsonrpc server1和连接自己的client代码，

进程B作为纯的client。

当进程A有状态需要通知时，A内部的client向自己的server发通知，这个信息就会被server转给所有的client.

这样就实现了进程A主动给进程B发送通知的机制。

有了这个，jsonrpc就可以替代dbus的功能来实现进程通信了。

## 如果处理需要很长时间

如果rpc函数处理需要很长的时间。

会影响其他的client的处理？

卡多次时间会被判断为通信失败呢？（这个应该没事）

2022年12月3日09:04:27

这个我也已经找到解决方法了。有些耗时的操作，靠server这个用一个event_handler的机制去处理实际操作。

先直接返回成功的。

# opensips里的jsonrpc

2022年12月3日09:06:05

今天在搜索我电脑上的jsonrpc相关文件的时候，看到我之前下载的opensips代码目录里也有jsonrpc的代码。

看看实现了什么。

看代码目录，opensips的代码还真是非常规范。值得一读。

每个代码目录的README就是很规范的代码文档。看起来很清晰严谨。

```
输出参数：
	connection_timeout
	write_timeout
	read_timeout
输出函数
	jsonrpc_request
	jsonrpc_notification
	

```

这个实现的是jsonrpc client的功能。

通过tcp发送请求给server。

# notification怎么发

没有id的就是notification。

server对notification的处理就是，不进行回复。

https://docs.actian.com/openroad/6.2/index.html#page/ServerRef/JSON-RPC_Notifications.htm

# 参考资料

1、JSON-RPC 2.0 Specification

https://www.jsonrpc.org/specification

2、【基础】RPC、JSON-RPC和HTTP区别

https://blog.csdn.net/chenguolinblog/article/details/90607551

3、python-jsonrpc框架实现JsonRPC协议的web服务

https://www.cnblogs.com/liangzp/p/9088792.html

4、WEB开发中，使用JSON-RPC好，还是RESTful API好？

https://www.zhihu.com/question/28570307

5、中文文档

http://static.kancloud.cn/thinkphp/json-rpc-2/43545