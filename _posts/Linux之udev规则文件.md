---
title: Linux之udev规则文件
date: 2017-08-05 14:48:45
tags:
---

udev的工作是靠kernel发出的uevent来驱动的，如果是删除的uevent，就会删除对应的节点。如果是增加设备的uevent，就会增加对应的节点。

规则文件是放在/etc/udev/rules.d目录下的。下面的文件命名规则是：xx-yy.rules。xx是数字，yy是字母，后缀都是rules。

执行时，先看数字，后看字母，后执行的会覆盖先执行的。



