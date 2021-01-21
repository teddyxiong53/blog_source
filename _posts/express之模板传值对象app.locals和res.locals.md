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



参考资料

1、Express 模板传值对象app.locals、res.locals

https://itbilu.com/nodejs/npm/Ny0k0TKP-.html

2、express中的res.locals和app.locals的使用

https://blog.csdn.net/yunchong_zhao/article/details/107204817