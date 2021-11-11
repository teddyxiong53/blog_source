---
title: nodejs之写一个博客
date: 2018-12-19 22:25:24
tags:
	- nodejs

---



根据github上的一个教程来做的。

# 最简单的网站

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

```
teddy@teddy-ThinkPad-SL410:~/work/nodejs/myblog$ tree routes/
routes/
├── index.js
└── users.js

0 directories, 2 files
teddy@teddy-ThinkPad-SL410:~/work/nodejs/myblog$ ls
index.js  node_modules  package.json  package-lock.json  routes
```



# 模板引擎

我们就用ejs这个引擎。

先安装。

```
npm install --save ejs
```

代码放在这里了。

https://github.com/teddyxiong53/nodejs_code/tree/master/express/myblog_code/01

ejs常用的标签有3种：

```
1、<% code %>：运行js代码，不输出。
2、<%= code %>：显示转义后的html内容。相当于不解析html标签，直接把标签显示。
3、<%- code %>：显示原始html内容。会解析标签。
```

举个例子：

```
fruit = ['apple', 'banana', 'pear'];
```

```
<ul>
	<% for(var i=0; i<fruit.length; i++) { %>
	<li><%= fruit[i] %></li>
	<% } %>
</ul>
```

得到的结果是：

````
<ul>
	<li>apple</li>
	<li>banana</li>
	</li>pear</li>
</ul>
````

## include

使用模板，肯定不是每个页面都定义一个模板，那么就失去了模板的意义了。

正确的做法的把模板拆分为片段来组合使用。

我们新建header.ejs和footer.ejs。修改users.ejs。



# express浅析

前面我们讲了路由和引擎的用法，但是express的精髓不在于此。

而在于中间件的设计理念。

express的中间件就是用来处理request的，当一个中间件处理完之后，就调用next()传递给下一个中间件。

如果不调用next，就不会继续传递了。

app.use就是使用中间件的。

我们看一个例子。我们把index.js写成这样。

```
const express = require("express");
const app = express()

app.use(function(req, res, next) {
    console.log(1)
    next()
})

app.use(function(req, res, next) {
    console.log(2)
    res.status(200).end()
})

app.listen(8080)
```

访问的时候，命令行终端会打印1和2 。

```
Starting child process with 'node index.js'
1
2
```

express上有很多的第三方中间件，我们应该先看看上面有没有可以满足我们要求的东西，避免重复造轮子。



# 开始正式开写博客项目

我们把前面的东西都删掉。

node_modules目录别删，以免重复下载。麻烦。

```
npm init
```

得到package.json文件。

新建目录结构如下：

```
teddy@teddy-ThinkPad-SL410:~/work/nodejs/myblog$ ls
index.js  models  node_modules  package.json  public  routes  views
```

安装需要的模块：

```
npm install config-lite connect-flash connect-mongo ejs express express-session marked moment mongolass objectid-to-timestamp sha1 winston express-winston --save
```

现在的package.json如下：

```
teddy@teddy-ThinkPad-SL410:~/work/nodejs/myblog$ cat package.json 
{
  "name": "myblog",
  "version": "1.0.0",
  "description": "",
  "main": "index.js",
  "dependencies": {
    "config-lite": "^2.1.0",
    "connect-flash": "^0.1.1",
    "connect-mongo": "^2.0.3",
    "ejs": "^2.6.1",
    "express": "^4.16.4",
    "express-formidable": "git+https://github.com/utatti/express-formidable.git",
    "express-session": "^1.15.6",
    "express-winston": "^3.0.1",
    "marked": "^0.5.2",
    "moment": "^2.23.0",
    "mongolass": "^4.4.1",
    "objectid-to-timestamp": "^1.3.0",
    "sha1": "^1.1.1",
    "winston": "^3.1.0"
  },
  "devDependencies": {},
  "scripts": {
    "test": "echo \"Error: no test specified\" && exit 1"
  },
  "author": "",
  "license": "ISC"
}
```

各个模块的功能：

1、express。web框架。

2、express-session。session中间件。

3、connect-mongo。把session存放在mongodb，跟express-session结合使用。

4、connect-flash。页面通知。基于session实现。

5、ejs。模板。

6、express-formidable。接收表单及文件上传。

7、config-lite。读取配置文件。

8、marked。markdown解析。

9、moment。时间格式化。

10、mongolass。mongodb驱动。

11、objectid-to-timestamp。根据ObjectId生成时间戳。

12、sha1。sha1加密。

13、winston。日志。

14、express-winston。express里的Winston中间件。

## eslint

代码检查工具。可以在编写代码阶段就帮助我们发现低级错误。

需要结合编辑器工作。

vscode里安装插件eslint。



# 配置文件

不管项目大小，把配置跟代码分离都是一个好的习惯。

一般把配置写在config.js或者config.json文件里。

config-lite是一个轻量的读取配置文件的模块。

会根据环境变量NODE_ENV加载不同config目录下的配置文件。

支持js、json、node、yml、yaml等后缀。

如果我们这样启动程序：

```
NODE_ENV=test node app
```

那么config-lite就依次查找：

```
config/test.js
config/test.json
config/test.node
config/test.yml
config/test.yaml
```

并且合并default配置。

我们在myblog目录下，新建config目录。下面新建default.js。

代码如下：

```
module.exports = {
    port: 8080,
    session : {
        secret: 'myblog',
        key: 'myblog',
        maxAge: 2592000000
    },
    mongodb: 'mongodb://localhost:27017/myblog'
}
```

# 功能设计

在动手开发之前，我们需要先明确博客需要实现的功能。

设计如下：

```
1、注册
	注册页：GET /signup
	注册： POST /signup
2、登陆
	登陆页： GET /signin
	登陆： POST /sigin
3、登出：GET /signout
4、查看文章
	主页： GET /posts
	个人主页： GET /post?author=xxx
	查看一篇文章： GET /posts/:postid
5、发表文章
	发表文章页： GET /posts/create
	发表文章： POST /posts/create
6、修改文章
	修改文章页： GET /posts/:postId/edit
	修改文章： POST /posts/:postId/edit
7、删除文章：GET /posts/:postId/remove
8、留言
	创建留言：POST /comments
	删除留言：GET /comments/:commentId/remove
	
```

由于我们的博客页面是后端渲染的，所以只通过简单的GET和POST跟后端进行交互。

如果使用jQuery或者其他前端框架（如vue、react等）可通过ajax跟后端交互。那么api设计就要尽量遵守restful风格。

# 会话

由于http是无状态的协议。所以服务端要记录用户的状态时，就需要用某种机制来识别具体的用户。

这个机制就是会话。

## cookie和session的区别

1、cookie在客户端。session在服务端。

2、session一般是基于cookie的，session id存放在cookie里。

3、session更加安全，cookie可以在本地查看和编辑。

# 页面通知

我们还需要这样的功能：

当我们操作成功的时候，需要显示一个成功的通知。

例如，登陆成功后，跳转到主页时，需要显示一个登陆成功的通知。

当我们操作失败的时候，需要显示一个失败的通知。

例如，注册的时候，如果用户名被占用了，需要显示用户名被占用的通知。

通知只显示一次，刷新后消失。

connect-flash就是用来完成这个工作的。

connect-flash是基于session实现的。

它的原理很简单，

```
1、设置初始值req.session.flash={}
2、通过req.flash(name, value)设置这个对象下的字段和值。
3、通过req.flash(name)获取这个对象下的值，同时删除这个字段，实现了只显示一次刷新后消失的效果。
```



# 权限控制

不管是论坛还是博客网站，我们没有登录的话，就只能浏览，登录后才能发帖或者写文章。

即使登录了，也不能删除修改别人的文章。

这个就是权限控制。

我们可以把用户的状态检查封装成一个中间件。在每个需要权限控制的路由加载这个中间件。

这样就可以实现权限控制。

在myblog目录下新建middlewares目录。在该目录下新建check.js。

代码如下：

```
module.exports = {
    checkLogin: function checkLogin(req, res, next) {
        if(!req.session.user) {
            req.flash('error', '未登录')
            return res.redirect('/signin')
        }
        next()
    },
    checkNotLogin: function checkNotLogin(req, res, next) {
        if(req.session.user) {
            req.flash('error', '已登录')
            return res.redirect('back')
        }
        next()
    }
}
```

checkNotLogin，这个是为了禁止用户在登陆状态访问注册、登陆界面。

接下来我们写路由文件。

routes/index.js。

写完放在这里。基本的架子有了。可以运行。

https://github.com/teddyxiong53/nodejs_code/tree/master/express/myblog_code/03



# 写界面

就是写css文件和ejs文件。



# 连接数据库

在myblog目录下新建lib目录。该目录下新建mongo.js。

代码如下：

```
const config = require('config-lite')(__dirname)
const Mongolass = require('mongolass')
const mongolass = new Mongolass()

mongolass.connect(config.mongodb)
```



# 注册

## 用户模型设计

name、passwd、avatar、gender、bio。



首先，我们来完成注册。

新建views/signup.ejs。



```
(node:4521) UnhandledPromiseRejectionWarning: TypeError [ERR_INVALID_CALLBACK]: Callback must be a function
```

这个是因为现在unlink的回调函数必选的了。所以需要这样改一下代码。

```
        fs.unlink(req.files.avatar.path, function (err) {
            if(err) {
                console.log('xhl -- unlink failed')
                throw err;
            }
        })
```

现在可以注册成功了。

放在这里了：https://github.com/teddyxiong53/nodejs_code/tree/master/express/myblog_code/05

# 登陆和登出

写完了。



# 文章模型

4个属性：

1、author。

2、title。

3、content。

4、pv。点击量。page view。





# 运行测试

我其实没有耐心写了。

把代码下载下来，放在Ubuntu下。

1、安装mongodb。

2、npm install

3、node index.js

运行正常。

可以支持用markdown写文章。



````
admin   (empty)
local   0.078GB
myblog  0.078GB
> use myblog
switched to db myblog
> show collections
comments
posts
sessions
system.indexes
users
> db.comments.find()
{ "_id" : ObjectId("5c218a3525cfd259e504ca5a"), "author" : ObjectId("5c218a1325cfd259e504ca58"), "postId" : ObjectId("5c218a2725cfd259e504ca59"), "content" : "111111111" }
> db.sessions.find()
{ "_id" : "xHDJJsZcJbhABTpgHubY6V3yfNJQ5hET", "session" : "{\"cookie\":{\"originalMaxAge\":2591999999,\"expires\":\"2019-01-24T01:37:11.930Z\",\"httpOnly\":true,\"path\":\"/\"},\"flash\":{}}", "expires" : ISODate("2019-01-24T01:37:11.930Z") }
{ "_id" : "mKXj8T9z9pIIQhd-1DKphEnGhirCgcwB", "session" : "{\"cookie\":{\"originalMaxAge\":2592000000,\"expires\":\"2019-01-24T01:39:54.849Z\",\"httpOnly\":true,\"path\":\"/\"},\"flash\":{},\"user\":{\"name\":\"aaa\",\"gender\":\"m\",\"bio\":\"aaa\",\"avatar\":\"upload_1762e241d233c7c19d5abb62d9d12c80.png\",\"_id\":\"5c218a1325cfd259e504ca58\"}}", "expires" : ISODate("2019-01-24T01:39:54.849Z") }
> db.system.indexes.find()
{ "v" : 1, "key" : { "_id" : 1 }, "name" : "_id_", "ns" : "myblog.sessions" }
{ "v" : 1, "key" : { "expires" : 1 }, "name" : "expires_1", "ns" : "myblog.sessions", "expireAfterSeconds" : 0 }
{ "v" : 1, "key" : { "_id" : 1 }, "name" : "_id_", "ns" : "myblog.users" }
{ "v" : 1, "unique" : true, "key" : { "name" : 1 }, "name" : "name_1", "ns" : "myblog.users" }
{ "v" : 1, "key" : { "_id" : 1 }, "name" : "_id_", "ns" : "myblog.comments" }
{ "v" : 1, "key" : { "postId" : 1, "_id" : 1 }, "name" : "postId_1__id_1", "ns" : "myblog.comments" }
{ "v" : 1, "key" : { "_id" : 1 }, "name" : "_id_", "ns" : "myblog.posts" }
{ "v" : 1, "key" : { "author" : 1, "_id" : -1 }, "name" : "author_1__id_-1", "ns" : "myblog.posts" }
> db.users.find()
{ "_id" : ObjectId("5c218a1325cfd259e504ca58"), "name" : "aaa", "password" : "061985f321210a2d6ef6d39dd66e73b8da2f29c5", "gender" : "m", "bio" : "aaa", "avatar" : "upload_1762e241d233c7c19d5abb62d9d12c80.png" }
````



# 参考资料

1、N-blog

https://github.com/nswbmw/N-blog