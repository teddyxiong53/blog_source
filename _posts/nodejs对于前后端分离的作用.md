---
title: nodejs对于前后端分离的作用
date: 2019-05-09 15:03:11
tags:
	- nodejs
---

1

很多公司的业务架构是，用nodejs作为前后端的中间层。

后端出于性能和别的原因，提供的接口所返回的数据格式也许不太适合前端直接使用。

前端所需的排序功能、筛选功能，以及到了视图层的页面展现，也许都需要对接口所提供的数据进行二次处理。

这些处理虽可以放在前端来进行，但也许数据量一大便会浪费浏览器性能。

因而现今，增加node端便是一种良好的解决方案。

nodejs在这里的作用就相当于一个代理。



大公司的老项目，存在这样一些问题。

1、前端代码越来越复杂。

2、前后端依然高度耦合。

3、无法很好地适配多种终端。



前端渲染也有不少的问题。





参考资料

1、

https://cnodejs.org/topic/565ebb193cda7a91276ff887

2、从NodeJS搭建中间层再谈前后端分离

https://blog.csdn.net/baidu_31333625/article/details/66970196

3、淘宝的前后端分离实践

https://2014.jsconfchina.com/slides/herman-taobaoweb/index.html#/

4、

https://juejin.im/post/5a68437b6fb9a01ca47aabc6