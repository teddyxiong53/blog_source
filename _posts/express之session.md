---
title: express之session
date: 2020-12-28 21:13:11
tags:
	- nodejs

---

1

session用于在服务端保存用户会话状态。

例如用户登陆信息等。

session在程序重启、多进程运行、负载均衡、跨域等情况下，会出现session丢失、多进程、多个站点之间不能共享的问题。

要解决这个问题，就需要对session进行持久化。

redis就是实现session持久化一个常用的方案。



因为http是无状态协议，所以提出了cookie，用来实现client和server之间的状态共享。

但是cookie存在这些问题：

1、cookie存储在客户端，可能被恶意修改。

2、而且每次带着cookie，增加了数据量。

而session把主要数据存放在server端，cookie这边，只需要带上一个sessionId就可以了。

这样既解决了安全性问题，也减小了client和server之间不必要的数据交换。

但是session也有它的问题，

最显著的就是默认存放在内存里，这样就容易丢失。

所以有必要对session进行持久化。

在express里使用redis保存session，需要3个模块：

```
npm i -s redis connnect-redis express-session
```



参考资料

1、Express.js(Node.js) 配置Redis持久化存储Session会话

https://itbilu.com/nodejs/npm/VJw-hEBhx.html