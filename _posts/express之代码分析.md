---
title: express之代码分析
date: 2019-05-10 17:11:11
tags:
	- nodejs

---

1

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



参考资料

1、

