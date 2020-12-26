---
title: express之代码分析
date: 2019-05-10 17:11:11
tags:
	- nodejs

---



代码在这里：https://github.com/expressjs/express

```
hlxiong@hlxiong-VirtualBox:~/work/test/express/express/lib$ tree
.
├── application.js
├── express.js
├── middleware
│   ├── init.js
│   └── query.js
├── request.js
├── response.js
├── router
│   ├── index.js
│   ├── layer.js
│   └── route.js
├── utils.js
└── view.js
```

主要代码就这些。

express.js是入口文件。

主要的组成部分有：

```
application
router
route
request 
response
```

express.js的输出就是一个函数。

```
exports = module.exports = createApplication;
```

然后给这个函数增加了一些属性。

```

```



我看到array-flatten，这个模块只有一个功能。

我看lodash里，有函数可以实现这个功能。

为什么不用lodash？

我测试了一些，作用还是不一样。

```
var flatten = require("array-flatten")
var arr = [1,[2,[3,[4]]]]

var ret = flatten(arr)
console.log(ret)

var _ = require("lodash")
ret = _.flatten(arr)
console.log(ret)
```

```
[ 1, 2, 3, 4 ]
[ 1, 2, [ 3, [ 4 ] ] ]
```



req的内容有哪些？

对象内容挺多的。

重要的有

```
url: '/',
method: 'GET',
headers:
baseUrl: '',
originalUrl: '/',
_parsedUrl:
Url {
    protocol: null,
    slashes: null,
    auth: null,
    host: null,
    port: null,
    hostname: null,
    hash: null,
    search: null,
    query: null,
    pathname: '/',
    path: '/',
    href: '/',
    _raw: '/' },
params: {},
query: {},
```

res跟req的差不多。

而且他们互相持有对方的引用。

res

```
locals

```



examples目录值得看看。



默认的app.locals的内容

```
{ settings:
   { 'x-powered-by': true,
     etag: 'weak',
     'etag fn': [Function: generateETag],
     env: 'development',
     'query parser': 'extended',
     'query parser fn': [Function: parseExtendedQueryString],
     'subdomain offset': 2,
     'trust proxy': false,
     'trust proxy fn': [Function: trustNone],
     view: [Function: View],
     views: '/home/hlxiong/work/test/express/test/views',
     'jsonp callback name': 'callback' } }
```



# express和connect关系

connect的代码：https://github.com/senchalabs/connect/

实际上只有一个文件。index.js。

里面只有几个函数。

![image-20201226105040739](../images/random_name/image-20201226105040739.png)

```
var proto = {}

var createServer = function () {}

proto.use = function () {}

proto.handle = function () {}

proto.listen = function () {}
```



参考资料

1、深入理解connect/express

https://segmentfault.com/a/1190000012714389