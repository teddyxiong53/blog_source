---
title: shadowsocks之lightsocks分析
date: 2019-01-14 10:53:59
tags:
	- shadowsocks
	- 异步
---



lightsocks是用asyncio实现的简化版本的shadowsocks。

不是很实用，但是适合用来学习。

里面用了asyncio。也可以作为学习asyncio的材料。



加密

就是简单的把0到255 的，都加1处理。

0变成1，

1变成2，

255变成0



先在本地运行看看。

先运行服务端：

```
python3 ./lsserver.py --random  --save server.json
```

再运行客户端：

```
python3 lslocal.py -c server.json
```

另外在lslocal.py和lsserver.py都加上：

```
import logging
logging.basicConfig(logging.DEBUG)
```

这样才可以看到运行的打印。

然后开第三个命令行窗口。配置好代理。

然后wget下载百度的首页。

然后就可以看到lslocal和lsserver的打印了。



我现在对加密不关注。重点关注异步的执行过程。

所以把cipher.py里的decode函数和encode函数都改成空的。

现在就可以看到没有加密的通信过程了。



跑一下测试代码test_local.py。

在代码最后加上

```
if __name__ == '__main__':
	unittest.main()
```

运行：

```
python3 ./lightsocks/test_local.py 
```

```
lightsocks里学习到的知识点
1、namedtuple定义网络地址（ip port）组成。
2、约束参数为可调用对象类型。
	didLiten: typing.Callable=None
3、所有用到的asyncio函数有：
	asyncio.AbstractEventLoop
		loop参数类型注解。
	get_event_loop
		都只用这个默认的。
	new_event_loop
		测试代码里。
	ensure_future
		所有的async定义的函数，在调用的地方，都这样包起来。
		这个用得最多了。
	asyncio.gather
	task.add_done_callback(cleanUp)
	有些函数，是loop的成员，
		sock_recv(conn, BUFFER_SIZE)
		sock_sendall(conn, bs)
		sock_connect(remoteConn, self.remoteAddr)
		sock_accept(listener)
		sock_connect(dstServer, dstAddress)
		getaddrinfo(host, port)
		close()
		run_until_complete
		run_forever()
```

