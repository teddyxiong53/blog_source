---
title: nodejs之electron
date: 2018-12-21 16:02:17
tags:
	- nodejs
---







这个是个github开发的一个开源框架。

后端是nodejs，前端的chromium。

用来开发桌面程序。

github的atom和微软的vscode都基于electron开发的编辑器。

通过把nodejs和chromium合并到同一个运行时环境里。打包为各个os的应用。

electron的版本发布非常频繁。

当nodejs和chromium有更新的时候，都会发新的版本。



一个基础的electron包含3个文件：

1、package.json。

2、main.js。

3、index.html。



官网在这里：https://electronjs.org/

基于electron开发的软件有：https://electronjs.org/apps



先看HelloWorld的。

然后看一个实用的例子。

https://electronjs.org/apps/simplenote



# 结构分析

electron运行package.json里的main脚本的进程，叫做主进程。

在主进程里运行的脚本，通过创建web页面来展示用户界面。

一个electron应用有且仅有一个主进程。

由于electron用到了chromium来展示web界面，所以chromium的多进程框架也被使用到。

在普通的浏览器里，web页面通常运行在一个sandbox里，不允许接触原生资源。

但是electron的通过nodejs的支持，可以接触原生资源。



主进程和渲染进程的区别

主进程使用BrowserWindow实例来创建页面。

每个BrowserWindow实例都在自己的渲染进程里运行。

主进程管理所有的web页面和他们对应的渲染进程。

每个渲染进程都是独立，它只关心自己运行的web页面。

在web页面里操作原生资源是非常危险的。

渲染进程需要发消息给主进程来完成这种操作。

# 使用electron的API

electron在主进程和渲染进程里，提供了大量的API给开发者使用。

开发者只需要require这个模块：

```
const electron = require("electron");
```

所有的API都有一个属性，就是进程类型，有的API只能给主进程用。

在渲染进程里，一般会这样写。这个在主进程里不能这么写，会报未定义的错误的。

```
const {remote} = require("electron");
const {BrowserWindow} = remote;
const win = new BrowserWindow();
```



# 跟nodejs关系

所有可以在nodejs里调用的东西，在electron里也可以调用。

# 调试应用的方法



# 分发应用

1、先到这里下载打包的electron执行文件。

2、解压后，在resources目录下，新建app目录。把你写的html文件、js文件、json文件都放在app目录下。

然后双击electron.exe运行就好了。

上面说的是手动打包的方式。

我感觉有点不正常。

菜单栏没有出来。

可以用工具打包。



注意：

最好全局安装，这样就可以避免每次都要安装一次的麻烦。

```
npm install -g electron
```




参考资料

1、electron

https://zh.wikipedia.org/wiki/Electron_(%E8%BD%AF%E4%BB%B6%E6%A1%86%E6%9E%B6)

2、如何利用 Electron 开发一个桌面 APP

https://zhuanlan.zhihu.com/p/32765171



