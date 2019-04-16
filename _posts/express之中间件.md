---
title: express之中间件
date: 2019-04-16 16:04:11
tags:
	- nodejs

---



中间件函数可以访问req、res以及next。

在中间件函数里，可以做：

```
1、执行任何代码。
2、对req和res进行修改。
3、结束请求、响应循环。
4、调用堆栈里的下一个中间件。
```

如果当前中间件函数没有结束请求，那么就必须调用next，交给下一个中间件去处理。

```
var express = require("express")
var app = express();

var myLogger = function(req, res, next) {
    console.log("LOGGED");
    next();
}

app.use(myLogger)
app.get("/", function(req, res) {
    res.send("hello world")
})

app.listen(3000);
```

中间件的顺序很重要。

是从上到下处理的。



express是一个路由和中间件web框架。

其自身只有最基本的功能，主要靠中间件来完成任务。

中间件分类：

```
1、应用层中间件
2、路由层中间件
3、错误处理中间件。
4、内置中间件。
5、第三方中间件。
```

```
var app = express()
app.use() //这种就叫应用层中间件
```

```
var router = express.Router()
var app = express()

router.use() //这种就叫路由器中间件。
```

```
错误处理中间件，多一个error参数，在最前面。
app.use(function(err, req, res, next) {
    
});
```

```
内置中间件，现在只有express.static这一个了。
```



参考资料

1、使用中间件

https://expressjs.com/zh-cn/guide/using-middleware.html

2、编写中间件以用于 Express 应用程序

https://expressjs.com/zh-cn/guide/writing-middleware.html