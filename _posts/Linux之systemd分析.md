---
title: Linux之systemd分析
date: 2018-12-12 20:43:17
tags:
	- Linux
typora-root-url: ..\
---



现在大部分的linux的init程序都换成了systemd了。

但是这一套我不是很熟悉。我还是熟悉busybox里的那一套init。开机启动的东西是在/etc/init.d里的。

但是现在经常碰到跟systemd相关的东西，所以有必须进行一个系统深入的了解。



service命令是System V的。

systemctl是systemd的。



# 简介

systemd是新一代的linux下的init程序。

开发的目标是：提供更优秀的框架，以表示service之间的依赖关系。并以此实现启动时服务的并行启动。

与传统的init程序相比，systemd采用了这些新的技术：

1、采用socket激活与dbus激活式服务。

2、用cgroups取代pid来追踪进程。这样带来一个好处，就是两次fork之后生成的daemon进程也不会脱离systemd的控制。



触发systemd出现的直接原因是：

传统的sysvinit，启动脚本是顺序执行的，这个对于服务器来说无关紧要，因为服务器不会经常关机开机。

但是随着linux向桌面系统扩展，这个问题就变得非常严重了。

启动各种服务，必须要并行化。但是又要考虑有依赖关系的服务的启动的先后顺序。

正是在这样的历史背景下，systemd应运而生。

```
sysvinit是System V init的缩写。
```

systemd借鉴了macos系统的launchd的不少的理念。

systemd是一个庞大的系统。这也让它受到了不少的诟病，因为unix的原则就是一个工具只做一件事情。systemd做了一个大而全的东西，跟这个原则是冲突的。



![](/images/systemd架构.png)





systemd提供了对应sysvint的兼容性。

系统中已经存在的服务和进程不需要修改。这个降低了sysvinit向systemd迁移的成本。使得systemd替换现在系统成为可能。



# 日志服务

systemd自带了日志服务journald。这个journald的设计初衷是为了克服syslog的缺点的。



# 基础概念

系统在初始化的过程，需要做很多的事情：

1、启动服务。

2、配置，例如挂载文件系统。

这些事情，都被统一抽象为一个概念：unit。叫配置单元。

服务和配置都统一为配置单元。

unit类型有：

1、service。最常用。代表一个后台服务，例如sshd。

2、socket。每个socket有一个对应的unit。

3、device。

4、mount。

5、automount。

6、swap。

7、target。

8、timer。

9、snapshot。

10、path。

11、scope。

12、slice。



# 依赖关系

依赖关系带来了复杂性，依赖关系，其实就是耦合性。

systemd已经尽力在降低各个服务之间的依赖性，但是无法完全消除。

systemd为了处理好依赖关系，提供了一些机制。









# 文件目录

2个目录：

1、/etc/systemd/system。这个有软链接指向了/lib/systemd/system

2、/lib/systemd/system

我们从etc目录下的，选择几个简单的，做一个分析。

1、dbus-org.bluez.service 

2、syslog.service

```
teddy@teddy-ThinkPad-SL410:/etc/systemd/system$ cat dbus-org.bluez.service 
[Unit]
Description=Bluetooth service
Documentation=man:bluetoothd(8)
ConditionPathIsDirectory=/sys/class/bluetooth

[Service]
Type=dbus
BusName=org.bluez
ExecStart=/usr/lib/bluetooth/bluetoothd -C
NotifyAccess=main
#WatchdogSec=10
#Restart=on-failure
CapabilityBoundingSet=CAP_NET_ADMIN CAP_NET_BIND_SERVICE
LimitNPROC=1

[Install]
WantedBy=bluetooth.target
Alias=dbus-org.bluez.service
```

```
teddy@teddy-ThinkPad-SL410:/etc/systemd/system$ cat syslog.service 
[Unit]
Description=System Logging Service
Requires=syslog.socket
Documentation=man:rsyslogd(8)
Documentation=http://www.rsyslog.com/doc/

[Service]
Type=notify
ExecStart=/usr/sbin/rsyslogd -n
StandardOutput=null
Restart=on-failure

[Install]
WantedBy=multi-user.target
Alias=syslog.service
```



# 参考资料

1、systemd

https://baike.baidu.com/item/systemd/18473007

2、systemd (简体中文)

https://wiki.archlinux.org/index.php/Systemd_(%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87)

3、关于 systemd 的初步理解

https://www.linuxidc.com/Linux/2018-03/151291.htm