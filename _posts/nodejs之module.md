---
title: nodejs之module
date: 2019-05-07 14:08:17
tags:
	- nodejs
---



写一个app.js，里面就放一行代码：

```
console.log(module)
```

得到输出是这样：

```
hlxiong@hlxiong-VirtualBox ~/work/test/node $ node app.js
Module {
  id: '.',
  exports: {},
  parent: null,
  filename: '/home/hlxiong/work/test/node/app.js',
  loaded: false,
  children: [],
  paths:
   [ '/home/hlxiong/work/test/node/node_modules',
     '/home/hlxiong/work/test/node_modules',
     '/home/hlxiong/work/node_modules',
     '/home/hlxiong/node_modules',
     '/home/node_modules',
     '/node_modules' ] }
```

我们可以看到exports这个属性。



参考资料

1、



