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
4、params。函数的参数。没有则为[]
```

一个rpc响应，要有下面的字段。

```
1、jsonprc。版本号，固定为2.0
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



## 如果处理需要很长时间

如果rpc函数处理需要很长的时间。

会影响其他的client的处理？

卡多次时间会被判断为通信失败呢？（这个应该没事）





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