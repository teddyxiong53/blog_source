---
title: virtualbox（1）
date: 2020-04-20 10:17:01
tags:

	- 虚拟机

---

1

### 增加usb2.0和usb3.0支持

我安装的的是5.2.12版本的。用了很长时间了。也不想替换新版本。

现在电脑上插着U盘，想挂到virtualbox里的Ubuntu来进行操作。但是识别不了。

进入设置，看到默认是usb1.1的。选择为usb2.0或者usb3.0，会提示你需要安装扩展包。

扩展包需要版本匹配，如果版本不匹配，会安装失败。

这里找：https://www.virtualbox.org/wiki/Download_Old_Builds_5_2

勾选usb2.0的。

打开虚拟机，可以看到windows里弹出了usb安装提示。



参考资料

1、VirtualBox扩展包安装教程|VirtualBox扩展增强包怎么安装

https://www.cnblogs.com/jpfss/p/9156738.html