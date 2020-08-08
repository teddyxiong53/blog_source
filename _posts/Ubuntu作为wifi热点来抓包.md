---
title: Ubuntu作为wifi热点来抓包
date: 2020-08-04 11:44:47
tags:
	- Ubuntu

---

1

现在因为需要抓板端的包。板端是rtos的。没法抓包。

所以打算把Ubuntu笔记本作为热点，让板端连接到热点，在笔记本上进行抓包。

按照参考资料操作就可以了。

但是有一点问题，就是我设置了密码后，手机连接总是提示密码错误。

我就设置为无密码的方式。

网上说用wep加密方式，密码长度设置为10位，就可以的。

但是这个加密方式几乎是已经淘汰了，网络设备不支持，照样是连接不上。

网上有个脚本，叫create_ap的。试一下。

```
create_ap wlan0 eth0 thinkpad 88889999 --no-virt
```

运行这个程序的时候，提示hostapd没有。

```
sudo apt install hostapd
```

我看看之前的问题，是不是跟这个有关系。



参考资料

1、

https://www.cnblogs.com/king-ding/archive/2016/10/09/ubuntuWIFI.html

2、

https://forum.ubuntu.org.cn/viewtopic.php?t=374942

3、ubuntu开启wifi热点

https://www.cnblogs.com/kangronghu/p/6761909.html