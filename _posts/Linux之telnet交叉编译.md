---
title: Linux之telnet交叉编译
date: 2018-10-08 15:58:17
tags:
	- Linux

---



busybox里把telnet的关闭了。但是不方便重新编译busybox，所以想要找一个第三方的telnetd程序。

尝试了这些方式：

1、inetutils。这个需要被inetd启动。没有弄起来。麻烦。

2、utelnetd。这个死活没有找到代码。

最后用dropbear搞定的。



busybox里有telnetd的。

在buildroot下操作。

make busybox-menuconfig

选上telnetd的。

然后make busybox-rebuild。

然后重新生成文件系统就可以了。

但是为什么默认也要密码，而且密码是多少？

buildroot里的system配置里有可以配置密码的地方。

配置好密码重新烧录就好了。



参考资料

1、Buildroot login

https://wiki.in-circuit.de/index.php5?title=Buildroot_login

2、login and passwords

https://github.com/gcwnow/buildroot/wiki/login-and-passwords