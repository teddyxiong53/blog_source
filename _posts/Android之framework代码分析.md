---
title: Android之framework代码分析
date: 2019-04-03 13:58:04
tags:
	- Android

---



代码在这里下载：

https://github.com/aosp-mirror/platform_frameworks_base

目录

```
api
	几个txt文件，主要的是current.txt。里面是java代码，4.7M大。都是资源相关的声明。
cmds
	系统启动时要的各种命令的源代码。
	例如app_process。下面就一个app_main.cpp文件。
	也有些是java写的。
core
	这个下面大量java代码。
	是主要代码目录。
data
	各种字体等资源。
drm
	权限管理、数字内容解密。
graphics
	图像相关。
其他
```



framework定义服务端组件、客户端组件、接口。



参考资料

1、Android: Framework层理解(一)

https://blog.csdn.net/lyjIT/article/details/52472623





