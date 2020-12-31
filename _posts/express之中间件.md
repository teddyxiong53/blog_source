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



# 官方中间件

## body-parser

解析request body的。

## compression

决定response是否进行压缩。

## connect-rid

生成唯一的request id

没有什么用。

## cookie-parser

接受2个参数，参数1是secret，参数2是options。

参数都可以没有。

## cookie-session

简单的基于cookie的session。

一个用户回话，有两种主要的方式：

存在在client或者存放在server端。

cookie-session采取的是存放在client端。

而第三方的express-session则是放在server端。

cookie-session的特点：

1、不需要服务端的数据库等资源来进行存储。

2、可以简化某些负载均衡的场景。

3、可以用来存储一个轻量的session，减少server端的数据库查找。

看几个简单的例子。

### 记录浏览次数

```
var cookieSession = require('cookie-session')
var express  = require('express')
var app = express()

app.set('trust proxy', 1)
app.use(cookieSession({
  name: 'view_count',
  keys: ['key1', 'key2']
}))
app.get('/', function(req, res, next) {
  req.session.views = (req.session.views || 0) + 1
  res.send('已经浏览了 '+req.session.views + ' 次')
})
app.listen(8080)
```

## cors

跨域资源共享。

全站都共享。

```
var express  = require('express')
var cors = require('cors')
var app = express()
app.use(cors())

app.get('/', function(req, res, next) {
  res.json({
    msg: '全站都是跨域资源共享的'
  })
})
app.listen(8080)
```

单个route允许跨域。

```
app.get('/', cors(),function(req, res, next) {
  res.json({
    msg: '只有这个路由是跨域资源共享的'
  })
})
```

指定某个域名可以共享。

```
var corsOptions = {
  origin: 'http://only4u.tech',
  optionSuccessStatus:200
}

app.get('/', cors(corsOptions),function(req, res, next) {
  res.json({
    msg: '只有这个路由是跨域资源共享的'
  })
})
```

## csurf

保护网站不受跨站请求伪造攻击。

简单来说就是这样：

你登陆了支付宝，然后访问一个危险网站。危险网站可以从你的浏览器里拿到访问支付宝的cookie。危险网站的网页里，有js代码，就伪造你向支付宝发起请求。

而如果没有保护操作，支付宝无法分辨这个请求是不是你本文发起的。

这个是利用了网站对用户浏览器的信任。

csurf就是为了应对这种情况。

防范的手段主要有：

1、检查referer字段。http头里有一个referer字段，用来表明请求是从哪里来的。在处理敏感数据的时候，referer字段应该跟请求的地址在同一个域名下。这种方式，简单。但是如果浏览器有漏洞，就还是容易被攻破。

2、添加校验token。就是在表单里添加一个不可见的随机数。这个随机数不会保存在cookie。所以危险网站拿不到这个数据。请求如果不带这随机数，则服务端就认为访问无效。

```

var express  = require('express')
var csrf = require('csurf')
var bodyParser = require('body-parser')
const cookieParser = require('cookie-parser')
var app = express()
app.set('view engine', 'ejs')

var csrfProtection = csrf({
  cookie: true
})

var parseForm = bodyParser.urlencoded({
  extended: false
})
app.use(cookieParser())
app.get('/form', csrfProtection,function(req, res) {
  res.render('send', {
    csrfToken: req.csrfToken()
  })
})
app.post('/process', parseForm, csrfProtection, function(req, res) {
  res.send('正在处理数据')
})
app.listen(8080)
```

在views目录下，新建send.ejs文件。

```
<form action="/process" method="POST">
    <input type="hidden" name="_csrf" value="" >
    最喜欢的颜色: <input type="text" name="color">
    <button type="submit">提交</button>
</form>

```



这个访问会报错。

```
ForbiddenError: invalid csrf token
```

## errorhandler

## morgan

```
var express  = require('express')
var morgan = require('morgan')
var app = express()
app.use(morgan('combined'))
app.get('/', function(req, res) {
  res.send('hello world')
})
app.listen(8080)
```

combined表示一种格式。

是apache的格式化。

```
LogFormat "%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\"" combined 
```

我当前得到的打印

```
::1 - - [29/Dec/2020:08:48:05 +0000] "GET / HTTP/1.1" 200 11 "-" "Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14"
```

### 写入文件

```
var express  = require('express')
var morgan = require('morgan')
var fs = require('fs')

var app = express()
var accessLogStream = fs.createWriteStream('access.log')

app.use(morgan('combined', {
  stream: accessLogStream
}))
app.get('/', function(req, res) {
  res.send('hello world')
})
app.listen(8080)
```

### 文件rotate

```
var accessLogStream = fs.createWriteStream('access.log', {
	interval: '1d',//1天切一个文件
})
```

## multer

## serve-favicon

```
var express = require('express')
var favicon = require('serve-favicon')
var path = require('path')

var app = express()
app.use(favicon(path.join(__dirname, 'public', 'favicon.ico')))

// Add your routes here, etc.

app.listen(3000)
```

代码是这样，但是我加了没有起作用。



参考资料

1、使用中间件

https://expressjs.com/zh-cn/guide/using-middleware.html

2、编写中间件以用于 Express 应用程序

https://expressjs.com/zh-cn/guide/writing-middleware.html

3、官方中间件

http://expressjs.com/en/resources/middleware.html