---
title: Linux之系统升级机制
date: 2018-07-25 10:10:28
tags:
	- Linux

---



更新嵌入式设备最佳的方式是对整个镜像进行更新。

对于Linux，这个问题转化为对分区的更新。

所以分区要仔细考虑。

bootloader分区。尽量避免更新这个。

内核分区。除非有安全问题，否则不更新。

rootfs。一般是只读的。

用户分区。最需要更新的。



有两种可能的镜像更新：

1、对称。

```
有2个bootloader分区。2个kernel分区。2个rootfs分区。2个用户分区。
可以在更新过程中取消。
```

2、非对称。

```

```



基于镜像的更新软件有：

1、swupdate。

2、RAUC。





# 参考资料

1、嵌入式 Linux 软件更新机制及架构汇总

https://www.aliyun.com/jiaocheng/121425.html

2、IoT固/软件更新及开源选项

https://blog.csdn.net/wireless_com/article/details/79548091

3、【IoT】如何实现 ESP32 固件的 OTA 在线升级更新

https://blog.csdn.net/liwei16611/article/details/81051909

可在线OTA升级的嵌入式系统设计方案

https://blog.csdn.net/zhou_chenz/article/details/54917622

基于Flask搭建Android应用OTA升级服务

https://blog.csdn.net/zjt19870816/article/details/80917529

嵌入式定制常用的实时Linux改造方案

https://blog.csdn.net/qq_34003774/article/details/80591716

260亿物联网终端，或将使OTA升级独成一个产业

http://www.sohu.com/a/214389286_472880

OTA升级如何实现？全解共享单车OTA升级过程

https://www.sohu.com/a/231352656_100093632

【迷你强的物联网】起始篇-简介与MQTT服务器【从零开始搭建自己的物联网系统】

https://blog.csdn.net/relijin/article/details/73274739