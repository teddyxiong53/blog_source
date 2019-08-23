---
title: nodejs之cnode论坛代码分析
date: 2019-04-16 15:15:28
tags:
	 - nodejs
---

1

代码在这里：

https://github.com/cnodejs/nodeclub



安装依赖：mongodb、redis。

```
sudo apt-get install redis-server
```

这个是基于Makefile来做的。

make intall。安装依赖模块。

make test，测试一下。

把config.default.js改名为config.js，修改host为0.0.0.0 。

然后node app.js运行。

可以正常访问。



涉及的主要数据库模型有：

user

topic

reply

topic_collect

message



user和topic比较复杂，其余几个简单。



proxy目录下的东西，是起什么作用？

相当于是封装了一些函数。代理模式。



顺着app.js看。

```
1、使用requestLog中间件。
	记录访问时间。
2、使用渲染时间记录中间件。
3、使用proxy中间件。
	这个是网络代理。但是没有看出什么。
	对于gravatar和Google网址，进行了特殊处理。
	
```

cnode论坛的作者，用了不少自己写的模块。可以学习一下。



参考资料

1、



