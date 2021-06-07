---
title: gui之electron
date: 2021-05-31 10:44:11
tags:
	- gui

---

--

这篇文章有提到在嵌入式系统上跑electron。

我可以尝试在buildroot上自己来跑一下。

https://toradex.tumblr.com/post/166740307858/creating-graphical-interfaces-for-embedded-linux

```
opkg update
opkg install libxss1 libcups2 nodejs nodejs-npm git

mkdir electron
cd electron
npm init
npm install electron-prebuilt

mkdir Samples
cd Samples
git clone https://github.com/hokein/electron-sample-apps.git
```

buildroot里可以安装npm吗？

有对应的package。

这个并没有什么奇怪的。OpenWrt都有的。

那么就可以试一下。

