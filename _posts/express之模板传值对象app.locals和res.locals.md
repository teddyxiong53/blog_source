---
title: express之模板传值对象app.locals和res.locals
date: 2019-05-11 13:46:11
tags:

	- nodejs
---



locals是express里，app对象和res对象的属性。

这个属性是一个对象，它的主要作用是把值传递到渲染的模板里。

app.locals.xx = "aa"

这样在ejs模板里，只需要使用xx的变量名就可以了。写起来就比较简略。



参考资料

1、Express 模板传值对象app.locals、res.locals

https://itbilu.com/nodejs/npm/Ny0k0TKP-.html

