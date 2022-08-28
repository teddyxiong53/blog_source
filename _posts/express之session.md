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

# cookie-session和express-session对比

这2个都是express里可以使用的session中间件。

它们分别有什么特点？区别是什么？

express-session功能更完善。支持session存储到磁盘上。

cookie-session简单，轻量，所有的数据都存放在浏览器这一边。

所以它们的主要区别就是：session存放的位置。

cookie-session适合的场景：

1、服务端没有使用数据库的情况。

2、简化某些负载均衡的场景。

3、减轻服务端的负载。





https://github.com/expressjs/cookie-session

```
A user session can be stored in two main ways with cookies: on the server or on the client. This module stores the session data on the client within a cookie, while a module like express-session stores only a session identifier on the client within a cookie and stores the session data on the server, typically in a database.
```

cookie-session用法

```
var cookieSession = require('cookie-session')
app.use(cookieSession({
	name: 'mysession',
	keys: ['abcd'],
	maxAge: 24*60*60*1000,//24h
}))
```



https://www.cnblogs.com/chyingp/p/nodejs-learning-express-session.html



参考资料

1、Express.js(Node.js) 配置Redis持久化存储Session会话

https://itbilu.com/nodejs/npm/VJw-hEBhx.html

2、What's difference with express-session and cookie-session?

https://stackoverflow.com/questions/23566555/whats-difference-with-express-session-and-cookie-session