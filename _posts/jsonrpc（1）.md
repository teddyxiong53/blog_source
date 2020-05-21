---
title: jsonrpc（1）
date: 2020-04-29 13:49:08
tags:
	- json

---

1

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





参考资料

1、JSON-RPC 2.0 Specification

https://www.jsonrpc.org/specification

2、【基础】RPC、JSON-RPC和HTTP区别

https://blog.csdn.net/chenguolinblog/article/details/90607551

3、python-jsonrpc框架实现JsonRPC协议的web服务

https://www.cnblogs.com/liangzp/p/9088792.html