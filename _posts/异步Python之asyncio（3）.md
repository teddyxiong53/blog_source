---
title: Python之asyncio（3）
date: 2019-11-14 17:37:48
tags:
	- Python

---

1

目前对asyncio还没有真正理解。

所以通过例子来加深认识。

写一个tcp client，基于asyncio。

准备服务器：

```
python3 -m http.server
```

这样就启动了一个简单的http服务器。很方便。

写client代码，如下：

```
import asyncio
HOST='192.168.56.101'

class ClientProtocol(asyncio.Protocol):
    def __init__(self, loop):
        self.loop = loop

    def connection_made(self, transport):
        request = 'GET / HTTP/1.1\r\nHost: {}\r\n\r\n'.format(HOST)
        transport.write(request.encode())

    def data_received(self, data):
        print(data.decode())

    def connection_lost(self, exc):
        self.loop.stop()

async def main(loop):
    await loop.create_connection(
        lambda : ClientProtocol(loop), HOST, 8000
    )

loop = asyncio.get_event_loop()
loop.run_until_complete(main(loop)) #其实运行2两次。不太合适，后面要改。
loop.run_forever() # 
```

上面这个代码，在connection_made里，手动构建了http请求，无疑是非常不灵活的。

我们新建一个ClientSession类。

```

```



参考资料

1、Python 的异步 IO：Asyncio 之 TCP Client

https://segmentfault.com/a/1190000012286062