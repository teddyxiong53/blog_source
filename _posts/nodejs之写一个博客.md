---
title: nodejs之写一个博客
date: 2018-12-19 22:25:24
tags:
	- nodejs

---



根据github上的一个教程来做的。

#最简单的网站

新建目录myblog。然后npm init。填入信息。

安装express。

```
node install express 
```

当前我安装的是4.16的。

新建index.js。

```
const express = require("express");
const app = express();

app.get("/", function(req, res) {
    res.send("hello, express");
});
app.listen(8080)
```

访问这个地址：http://192.168.0.6:8080/

# supervisor

为了提高开发效率，我们需要需要修改后，不要重新启动程序就可以看到效果。

这个是可以做到的。

需要安装一个模块。

```
sudo npm install -g supervisor
```

然后用supervisor index.js来启动程序。



# 路由

修改index.js如下：

```
const express = require("express");
const app = express();

app.get("/", function(req, res) {
    res.send("hello, express ");
});
app.get("/users/:name", function(req, res) {
    res.send("hello " + req.params.name);
})
app.listen(8080)
```

访问：http://192.168.0.6:8080/users/xhl

当前我们的路由很少，所以都放在index.js里，看起来也还好。

但是实际项目的路由会很多。

现在我们在myblog目录下，新建一个routes目录。下面新建index.js和users.js 2个文件。



# 参考资料

1、N-blog

https://github.com/nswbmw/N-blog