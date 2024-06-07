---
title: Linux之session
date: 2018-09-22 22:47:20
tags:
	- Linux

---



在跟dbus打交道的过程中，深感需要把linux的session理解透彻。

# dbus-launch和dbus-run-session区别是什么？

我们在buildroot的系统里，为什么需要手动执行dbus-launch？

应该是因为默认系统只在S01dbus里启动了dbus-daemon --system。而没有session方式的dbus-daemon。

而我们在应用里，使用的是session方式的dbus。所以就必须自己dbus-launch的方式启动dbus-daemon。

那么现在问题就是，系统可以启动多个dbus-daemon程序吗？

是可以的。

```
/etc/udev/rules.d # ps |grep dbus
 1595 root     /usr/bin/dbus-daemon --syslog --fork --print-pid 4 --print-address 6 --session
 1666 dbus     dbus-daemon --system
 5614 root     dbus-run-session pipewire
 5615 root     dbus-daemon --nofork --print-address 4 --session
 9664 root     /usr/bin/dbus-daemon --syslog --fork --print-pid 4 --print-address 6 --session
10634 root     /usr/bin/dbus-daemon --syslog --fork --print-pid 4 --print-address 6 --session
11975 root     grep dbus
```



# DBUS_SESSION_BUS_ADDRESS

这个环境变量的作用是什么？

在终端中键入以下命令：

```
eval `dbus-launch --auto-syntax`
```

其实dbus-daemon是有地址的，而且有一个环境变量来表示它--DBUS_SESSION_BUS_ADDRESS，

可以用命令env查看到。

我们的程序，也就就是依靠这个环境变量来确认使用哪一个dbus-daemon的。

 当我们登录进桌面环境的时候，系统启动脚本会调用到dbus-launch来启动一个dbus-daemon，同时会把这个dbus-daemon的地址赋予环境变量DBUS_SESSION_BUS_ADDRESS。





https://stackoverflow.com/questions/41242460/how-to-export-dbus-session-bus-address

# dbus-daemon

dbus-daemon, 

dbus-launch, 

dbus-send, 

dbus-monitor, 

dbus-cleanup-sockets, 

dbus-run-session, 

dbus-test-tool,

dbus-update-activation-environment, 

dbus-uuidgen.

这里面最常用的就是dbus-daemon,不然dbus不能使用．其他先不做了解，目前只会用到dbus-daemon．



系统启动之后，有两个dbus daemon的实例，　

一个称为system, 一个称为session(如果是多个用户，那么会每个用户启动一个)，

这个实例配置不同，权限也不同

－＞system 实例使用的配置文件＝/etc/dbus-1/system.conf
－＞session实例使用的配置文件=/etc/dbus-1/session.conf

目前我的buildroot下面的目录是这样：

```
/etc/dbus-1 # find -name "*"
.
./session.conf  只有一个空元素busconfig
./system.conf   只有一个空元素busconfig
./system.d  
./system.d/dnsmasq.conf  busconfig里有policy节点。
./system.d/org.freedesktop.ModemManager1.conf
./system.d/wpa_supplicant.conf
```



	root@june:~# dbus-daemon --session --print-address --nofork --print-pid
	unix:abstract=/tmp/dbus-ylwBCGyhmF,guid=bd7496f59ac6455852a455b45b398e03
	6943

这个看起来等价于dbus-launch。

https://blog.csdn.net/u012385733/article/details/80881343

# 开机

XDG_CONFIG_HOME

这个能看到。是哪里定义的？

```
etc/profile:43:    export XDG_CONFIG_HOME=/var
etc/init.d/rcS:15:export XDG_CONFIG_HOME=/var
```

这2个文件里，哪个有用？

还是都有用？

哪个先执行？



串口和adb shell里看到的情况还不一样。

应该adb shell没有登陆的过程。

所以profile没有执行。



# 参考资料

1、setsid

https://baike.baidu.com/item/setsid/384930