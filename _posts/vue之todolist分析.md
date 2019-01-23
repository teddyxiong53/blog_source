---
title: vue之todolist分析
date: 2019-01-23 16:07:55
tags:
	- vue

---



这个代码在这里：

http://www.runoob.com/wp-content/uploads/2018/11/vuepro.zip

先看看npm run dev做了什么？

```
webpack-dev-server --inline --progress --config build/webpack.dev.conf.js
```



webpack-dev-server这个是做什么呢？

使用一个server跟webpack一起。只能在开发阶段用。

可以支持动态重载，这样修改代码就可以直接看到变化。

安装：

```
npm install webpack-dev-server --save-dev
```

那么就看看webpack.dev.conf.js这个文件里写了什么。





参考资料

1、webpack-dev-server

https://github.com/webpack/webpack-dev-server