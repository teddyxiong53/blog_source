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

```
n-blog里，ejs文件里用的user、success、error这3个变量，从哪里传递过来的？
是在index.js里，有这样的代码：
// 添加模板必需的三个变量
app.use(function (req, res, next) {
  res.locals.user = req.session.user
  res.locals.success = req.flash('success').toString()
  res.locals.error = req.flash('error').toString()
  next()
})
这个相当于不管什么情况下都传递的。
```

`locals`可能存在于`app`对象中即：[`app.locals`](http://itbilu.com/nodejs/npm/VJ5TlyRnl.html#app-properties-locals)；

也可能存在于`res`对象中，即：[`res.locals`](http://itbilu.com/nodejs/npm/Vkp32gJpg.html#res-prop-locals)。

两者都会将该对象传递至所渲染的页面中。

不同的是，`app.locals`会在整个生命周期中起作用；

而`res.locals`只会有**当前请求中起作用。**

由于`app.locals`在当前应用所有的渲染模中访问，

这样我们就可以在该对象中定义一些顶级/全局的数据，

并在渲染模板中使用。



参考资料

1、Express 模板传值对象app.locals、res.locals

https://itbilu.com/nodejs/npm/Ny0k0TKP-.html

2、express中的res.locals和app.locals的使用

https://blog.csdn.net/yunchong_zhao/article/details/107204817