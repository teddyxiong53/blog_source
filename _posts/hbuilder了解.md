---
title: hbuilder了解
date: 2018-06-03 15:25:28
tags:
	- hbuilder

---



写html文件这些，我不太熟悉，所以用notepad++ 写起来就很痛苦。找一个好点的IDE来写。

看网上提到hbuilder这工具。下载看看。

#简介

是基于eclipse的，但是有部分代码是C写的，所以启动速度还可以。

DCloud面向HTML5行业分别推出了开发工具HBuilder、手机强化引擎5+ Runtime、跨平台前端框架mui、应用发行产品流应用，通过系列产品对HTML5的强化支持，使得HTML5能达到原生的功能和体验，同时在发行上更优于原生应用。



# helloworld之app

默认新建一个Hello H5+项目。

使用云打包的方式来提交给云端服务器帮你打包出一个apk来。然后自动下载下来，我们安装到手机上看看。可以正常工作。

那么我们做一个修改。

看看这个开发过程是怎样的。



# helloworld之web

可以部署到我的windows的IIS下运行。

很简单。







看默认生成的helloH5+ 的代码。

plus是什么？

https://ask.dcloud.net.cn/article/165

plus是5+Runtime的内部对象。

5+Runtime是dcloud开发的一个运行时。

http://www.dcloud.io/runtime.html



基本看懂了。写简单应用应该可以。



这个文档值得看。

https://ask.dcloud.net.cn/docs/



# 基本用法

## 基本

在文件上，单击预览。双击打开。

文件保存是免丢失的，还有热退出功能。

默认每30秒自动保存。

右键，新建页面，可以自动把目录都建好，并自动添加到pages.json文件里。



## 语法提示

点击右下角的语法提示库，可以选择。

![image-20210111095843115](https://gitee.com/teddyxiong53/playopenwrt_pic/raw/master/image-20210111095843115.png)

这个设置是针对项目的，勾选后，对整个项目起作用。

## 代码助手

代码提示的时候，可以按alt+数字来选择某一项，这样比按方向键会快一点。

## 快速帮助

把光标放到函数上，然后按一下F1，就可以打开这个函数的网页说明。

