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

