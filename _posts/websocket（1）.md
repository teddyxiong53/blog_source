---
title: websocket（1）
date: 2020-06-28 15:57:51
tags:
	- 网络

---

--

iflyos是使用了websocket跟服务端进行通信。所以需要把websocket进行学习。

# 简介

websocket是一种在tcp长连接上进行全双工通信的协议。

它的出现，使得服务端和客户端之间的数据交换变得容易。

允许服务端主动向客户端推送消息。

这个是传统http协议不支持而又非常需要的一个功能。

为了实现服务端对客户端的消息推送，传统的解决方法，是通过ajax轮询，这样非常耗费流量。效率及其低下。

浏览器通过JavaScript向服务器发出建立websocket连接的请求。

**WebSocket并非一个工具，而是HTML5里面的协议。**

它从某种角度上弥补了上一部分中我们介绍过的HTTP协议的缺陷。

由于使用WebSocket使用HTTP的端口，因此TCP连接建立后的握手消息是基于HTTP的，由服务器判断这是一个HTTP协议，还是WebSocket协议。 

WebSocket连接除了建立和关闭时的握手，数据传输和HTTP没有任何关系。

# 建立websocket连接

client向server发出http请求，带上header

```
GET /chat HTTP/1.1
Host: server.example.com
Upgrade: websocket # 重点是这里。
Connection: Upgrade
Sec-WebSocket-Key: x3JJHMbDL1EzLkh9GBhXDw==
Sec-WebSocket-Protocol: chat, superchat
Sec-WebSocket-Version: 13
Origin: http://example.com
```

然后server回复client。

```
HTTP/1.1 101 Switching Protocols
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Accept: HSmrc0sMlYUkAGmm5OPpG2HaGWk=
Sec-WebSocket-Protocol: chat
```

一次握手成功之后，客户端和服务器之间就可以建立持久连接的双向传输数据通道，而且服务器不需要被动地等客户端的请求，服务器这边有新消息就可以通知客户端，化被动为主动。

此外，使用WebSocket时，不会像HTTP一样无状态，服务器会一直知道客户端的身份。

服务器与客户端之间交换的标头信息也很小。

Websocket使用 `ws` 或 `wss` 的统一资源标志符，类似于 `HTTP` 或 `HTTPS`，其中 `wss` 表示在 TLS 之上的 Websocket ，相当于 HTTPS 了。如：

```
ws://example.com/chat
wss://example.com/chat
```



Nginx 自从 1.3 版本就开始支持 WebSocket 了，并且可以为 WebSocket 应用程序做反向代理和负载均衡。

默认情况下，Websocket 的 ws 协议使用 80 端口；运行在TLS之上时，wss 协议默认使用 443 端口。

```
客户端                                                 服务器
   |                                                       |
   |---- 发送握手请求（包含 Upgrade 和 Connection 头部字段） --->|
   |                                                       |
   |<--- 返回握手响应（包含 Upgrade 和 Connection 头部字段） ----|
   |                                                       |
   |---- 发送握手确认（包含握手密钥的哈希值） --->                |
   |                                                      |
   |<-------------- WebSocket 连接建立 --------------  |
   |                                                  |
   |--------------------- WebSocket 连接 --------------------|
   |                                                  |
   |                                               数据交换
   |                                                  |

```



# nopoll分析

nopoll是一个C语言写的很小的websocket库。

io复用机制是select的。

nopoll是linux常用的开源的websocket的实现。

安装成功后，只需要在我们的源文件中包含头文件nopoll.h

如果在多个线程中同时调用nopoll的api，需要设置4个回调用以执行nopoll的创建，销毁和上锁和解锁。

```
noPollPtr nopoll_freertos_mutex_create(void)
{
	OS_Mutex_t *mutex  = nopoll_new(OS_Mutex_t, 1);
	if (mutex == NULL)
		return NULL;

	if (OS_MutexCreate(mutex) == OS_OK)
		return mutex;
	else
		return NULL;
}

void nopoll_freertos_mutex_destroy(noPollPtr mutex)
{
	if (OS_MutexDelete(mutex) == OS_OK)
		nopoll_free(mutex);
}

void nopoll_freertos_mutex_lock(noPollPtr mutex)
{
	OS_MutexLock(mutex, 10000);
}

void nopoll_freertos_mutex_unlock(noPollPtr mutex)
{
	OS_MutexUnlock(mutex);
}

int nopoll_freertos_gettimeofday(struct timeval *tv, noPollPtr notUsed)
{
	return gettimeofday(tv, NULL);
}
```



使用nopoll接口创建一个简单的websocket server。

```
noPollConn *listener = nopoll_listener_new(ctx, "0.0.0.0", 1234);
if(!nopoll_conn_is_ok(listener)) {
	
}
nopoll_ctx_set_on_msg(ctx, listener_on_message, NULL);
nopoll_loop_wait(ctx, 0);
```

从websocket的链接上接收数据：

使用nopoll_loop_wait()循环等待，设置消息接收的处理函数（nopoll_ctx_set_on_msg 和nopoll_conn_set_on_msg）.



碰到一个棘手的问题。

就是设备端被服务端主动断开连接后。

nopoll函数会卡死。找到解决方法了。还是要使用nopoll_conn_is_ok和nopoll_conn_is_ready进行检查。



把nopoll的client例子都看一遍。

nopoll_conn_send_ping：这个是

```
nopoll_log_enable (ctx, debug);
```



# python下的server和client

Python里的websocket的package是

```
pip install websockets
```

新建server.py，写入下面的内容：

```
import asyncio
import websockets

async def handler(websocket, path):
    data = await websocket.recv()
    reply = f'recv data: {data}'
    await websocket.send(reply)

start_server = websockets.serve(handler, "0.0.0.0", 8000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
```

然后写一个client.html，内容如下：（html代码是vscode里输入html自动生成的，忽略。只看script部分的）

```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    <button onclick="contactServer">connect server</button>

</body>
<script>
    let socket = new WebSocket('ws://192.168.56.101:8000')
    socket.addEventListener('open', function(event) {
        socket.send('conn setup')
    })
    socket.addEventListener('message', function (event) {
        console.log(event.data)
    })
    let contactServer = ()=> {
        socket.send('init')
    }
</script>
</html>
```

然后直接打开client.html文件就可以测试。

我们也可以写一个python版本的client。

client.py

```
import asyncio
import websockets

async def test():
    async with websockets.connect('ws://localhost:8000') as websocket:
        await websocket.send("hello")
        response = await websocket.recv()
        print(response)

asyncio.get_event_loop().run_until_complete(test())
```





参考资料

1、How To Build WebSocket Server And Client in Python

https://www.piesocket.com/blog/python-websocket

# 参考资料

1、WebSocket

https://baike.baidu.com/item/WebSocket/1953845?fr=aladdin

2、Python3+WebSockets实现WebSocket通信

https://www.cnblogs.com/lsdb/p/10949766.html

3、

https://blog.csdn.net/antony9118/article/details/54343534

4、Nginx 支持websocket的配置

https://blog.csdn.net/weixin_37264997/article/details/80341911

5、WebSocket 结合 Nginx 实现域名及 WSS 协议访问

https://www.cnblogs.com/mafly/p/websocket.html

6、使用nopoll实现websocket的接口点用流程

https://blog.csdn.net/u010299133/article/details/91491344