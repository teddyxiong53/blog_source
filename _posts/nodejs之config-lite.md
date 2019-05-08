---
title: nodejs之config-lite
date: 2019-05-08 15:52:11
tags:
	- nodejs
---

1

这个很简单，看一看用来学习nodejs模块写法的材料。

先看看怎么用的。

安装：

```
npm install config-lite
```

新建文件目录如下：

```
hlxiong@hlxiong-VirtualBox ~/work/test/config-lite $ tree        
.
├── app.js
└── config
    └── default.js
```

default.js：

```
module.exports = {
    name: "xx",
    age: 10
}
```

app.js：

```
const config = require('config-lite')(__dirname)
console.log(config)
```

运行：

```
hlxiong@hlxiong-VirtualBox ~/work/test/config-lite $ node app.js
{ name: 'xx', age: 10 }
```

接下来，我以写代读。

本目录下，新建config-lite目录。

在config-lite目录下，npm init -y。

新建一个index.js文件。

目录结构：

```
.
├── app.js
├── config
│   └── default.js
└── config-lite
    ├── index.js
    └── package.json
```

需要这4个第三方模块。

```
const _ = require('lodash');
const chalk = require('chalk');
const resolve = require('resolve');
const argv = require('optimist').argv;
```

安装：

```
 npm install --save lodash chalk resolve optimist
```

在index.js里写入：

```
'use strict'

module.exports = function configLite(customOpt) {
    console.log(customOpt)
    return {}
}
```

这样，我们就有一个基本的架子了。

然后往里面填写东西。

总体内容很简单。就是用require把模块读取出来。

基本上可以不用这个模块。

你自己写一个config.js，导出一个对象就好了。





