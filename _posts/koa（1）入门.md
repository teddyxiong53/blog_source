---
title: koa（1）入门
date: 2019-05-09 14:46:11
tags:
	- nodejs

---



koa和express对比

```
Express
优点：线性逻辑，通过中间件形式把业务逻辑细分、简化，一个请求进来经过一系列中间件处理后再响应给用户，清晰明了。 
缺点：基于 callback 组合业务逻辑，业务逻辑复杂时嵌套过多，异常捕获困难。

Koa
优点：首先，借助 co 和 generator，很好地解决了异步流程控制和异常捕获问题。其次，Koa 把 Express 中内置的 router、view 等功能都移除了，使得框架本身更轻量。 
缺点：社区相对较小。
```



大概看了一下，暂时不学了。



参考资料

1、koa2 快速开始

https://chenshenhai.github.io/koa2-note/note/start/quick.html

2、

https://koa.bootcss.com/

3、Express和koa各有啥优缺点?

https://www.zhihu.com/question/38879363