---
title: express之ejs-mate
date: 2021-01-18 11:45:11
tags:
	- express

---

--

母版页之方便之处相信做过web开发的都不用说太多,

可以重复利用资源,维护方便,

开发起来你只需关注当前页变动的东西,

固定不变的全部放到母版页,

可以理解为前人栽树后人乘凉,省时,省力,省心.

ejs的母版页功能支持

需要依赖一个第三方包 **[ejs-mate](https://github.com/JacksonTian/ejs-mate)** 可以根据npm install ejs-mate 直接安装 

安装之后的使用方法：

```
var app = express();
app.set('view engine', 'html');
app.engine('html', require('ejs-mate'));
app.locals._layoutFile = 'layout.html';
```

上面指定ejs引擎渲染html 文件,

接着指定使用 ejs-mate 做母版页引擎,

最后指定 母版页是 layout.html

这里有个 app.locals 这个变量,

提一句,可以把 locals 理解成客户端的一个全局变量,

我们现在给变量的_alyoutFile 属性赋值 'layout.html'

如果上面最后一句你不写,需要在前端每个页面指定渲染的母版页,假设 index.ejs 套用母版页前代码如下:

```
<% layout('layout.html') -%>
<span>Hello World!</span>
```



参考资料

1、Express框架-母版ejs-mate

https://blog.csdn.net/weixin_41933298/article/details/88392689

2、ejs母版页让你的node.js应用开发更快更有效- 一介布衣

https://yijiebuyi.com/blog/08cf14e904325c19814465689453b3aa.html