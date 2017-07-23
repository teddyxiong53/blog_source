---
title: shadowsocks之kcp
date: 2017-07-23 13:53:49
tags:

	- shadowsocks

---

我的shadowsocks翻墙现在效果不好了。在google plus上提问，有人说用tcp加速，我现在研究一下。

# 1. 什么是kcp

1、这不是一个标准协议。是在tcp的基础上修改的。

2、以浪费10%到20%的流量来换取延时的降低。

3、使用还比较广泛。

4、作者是中国人。是一个游戏开发者。

5、代码量不大，就两个文件。itcp.c和itcp.h。



# 2. 如何在shadowsocks中使用kcp

基于kcp的有一个工具叫kcptun。

下载地址是这里。

https://github.com/xtaci/kcptun/releases/download/v20170525/kcptun-linux-amd64-20170525.tar.gz

下载到vps上，解压开来，是2个可执行文件。server_linux_amd64和client_linux_amd64 。

为了方便使用，我们把一些操作封装成脚本来用。

我配置了并没有支持工作。算了，不折腾了。

