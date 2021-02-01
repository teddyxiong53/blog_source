---
title: express之模板引擎
date: 2021-01-27 11:51:11
tags:
	- express

---

--

看了不少的express项目，发现大家是各种模板引擎都在用。所以还是把模板引擎梳理一下，方便阅读别人的项目代码。

支持的模板引擎有：

jade（默认），现在改名为pug了。这个受haml启发

haml.js。

ejs

dust.js

dot

mustache

handlerbars。

nunjunks

ejs-mate



发现有些用的模板，在官网都没有列出来。

例如：xtpl。



希望模板引擎提供这些特性：

1、支持模板继承extend。

2、支持模板扩展block。

3、支持模板组合。

4、支持预编译。

可以混合使用多种模板引擎。

只需要在render('index.jade')这样后面加上对应的后缀名就好了。



保证能看懂就好了。我主要还是用ejs的。



# pug

这个在所有的模板引擎里，算是最特别的。

因为它的结构，完全不像html的风格。

而是python风格的。

这个就不看了。不会用这个的。



参考资料

1、Express：模板引擎深入研究

https://www.cnblogs.com/chyingp/p/express-render-engine.html

2、

https://expressjs.com/en/resources/template-engines.html