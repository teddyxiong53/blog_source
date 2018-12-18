---
title: nodejs之Ubuntu升级到最新版本
date: 2018-12-18 20:11:24
tags:
	- nodejs

---



我在Ubuntu32位上，不能正常升级。

我用源代码的方式自己编译看看。

https://nodejs.org/en/download/

在这里下载源代码。

```
./configure
make
```

目前稳定版本是10.14的。

我先把我用apt-get安装的nodejs彻底卸载掉。

编译还比较耗时间。c++编译比较慢，文件又多。

估计要好几个小时，我在笔记本上编译，晚上不关机了。

```
teddy@teddy-ThinkPad-SL410:~/work/nodejs/node-v10.14.2$ node -v
v10.14.2
```



