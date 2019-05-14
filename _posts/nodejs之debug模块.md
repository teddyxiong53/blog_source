---
title: nodejs之debug模块
date: 2019-05-14 11:16:11
tags:
	- nodejs

---

1

先安装：

```
npm install debug
```

使用：

```
var debug = require("debug")('app')//注意后面跟的这个app
debug('hello debug')
```

运行：

```
DEBUG=app node app.js
```

结果：

```
  app hello debug +0ms
```

运行时，不加上DEBUG=app，则没有任何打印。



# namespace

传递给debug的那个参数，就是namespace。

```
var debug = require('debug')
var appDebug = debug('app')
var apiDebug = debug('api')

appDebug("app debug")
apiDebug("api debug")
```



运行：

```
hlxiong@hlxiong-VirtualBox:~/work/test/mongoose$ DEBUG=app,api node app.js
  app app debug +0ms
  api api debug +0ms
hlxiong@hlxiong-VirtualBox:~/work/test/mongoose$ DEBUG=app node app.js
  app app debug +0ms
```



排除某些日志打印。

```
var debug = require('debug')
var appDebug = debug('app')
var apiDebug = debug('api')
var loginDebug = debug('account:login')

appDebug("app debug")
apiDebug("api debug")
loginDebug("account debug")
```

要排除account相关的打印。则这样就可以。就用一个“-”。

```
DEBUG=*,-account* node app.js
```



参考资料

1、

https://juejin.im/post/58fe94e55c497d00580ca7c5

