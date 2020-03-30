---
title: Linux检测自己IP地址变化
date: 2020-03-27 09:18:11
tags:
	- Linux

---

1

现在一台嵌入式机器上运行snapserver，自己同时也运行了snapclient。

snapclient -h IP的方式来连接到snapserver的。

搜索出来是一个192.168.0.x这种ip地址。

机器放了几天，然后机器的ip地址从192.168.0.104变成了192.168.0.102 。

然后snapclient就找不到snapserver了。

所以，需要一种机制，让系统可以在自己ip地址发生变化的时候，应用层可以得到通知，然后主动重新启动snapclient连接到新的IP上。

自己写脚本进行查询当然也可以做到。但是这种方式太笨了。

这样的系统变化，肯定有一个主动的通知机制的。就像中断一样。



机器上运行的是dhcpcd程序来获取动态ip地址的。

dhcpcd可以注册钩子脚本。

钩子脚本的位置，不同的系统不相同。

我的机器上是buildroot编译出来的。是在/lib/dhcpcd目录下。

```
/lib/dhcpcd # ls -lh                                                     
drwxr-xr-x    2 root     root          30 Mar 26 17:51 dev               
drwxr-xr-x    2 root     root         105 Nov 21 10:33 dhcpcd-hooks      
-r-xr-xr-x    1 root     root        8.5K Nov 21 10:33 dhcpcd-run-hooks  
```

这个信息是从buildroot/package/dhcpcd/dhcpcd.mk文件里看到的。

```
define DHCPCD_CONFIGURE_CMDS
	(cd $(@D); \
	$(TARGET_CONFIGURE_OPTS) ./configure \
		--os=linux \
		--libexecdir=/lib/dhcpcd \
		$(DHCPCD_CONFIG_OPTS) )
endef
```

dhcpcd-run-hooks 这个是总脚本。内容较多。

我们不直接修改这个。

我们在dhcpcd-hooks目录下新增一个配置文件。

当前这个目录下有几个文件：

```
/lib/dhcpcd/dhcpcd-hooks # ls                   
01-test         20-resolv.conf  50-ntp.conf     
02-dump         30-hostname                     
```

看一下dhcpcd-run-hooks脚本。

里面是这样调用的，依次遍历这些文件。enter和exit的脚本，我的机器里没有。不管。

```
for hook in \
	/etc/dhcpcd.enter-hook \
	/lib/dhcpcd/dhcpcd-hooks/* \
	/etc/dhcpcd.exit-hook
```



# NetworkManager

这个太复杂了。不划算。需要引入太多东西。

providing detection and configuration for systems to automatically connect to networks.

NetworkManager prefers known wireless networks and has the ability to switch to the most reliable network. 
NetworkManager also prefers wired connections over wireless ones, 
NetworkManager was originally developed by Red Hat and now is hosted by the GNOME project.



# DBUS





参考资料

1、在Linux中检测IP地址的变化

https://www.thinbug.com/q/2738935

2、How to detect IP address change programmatically in Linux?

https://stackoverflow.com/questions/579783/how-to-detect-ip-address-change-programmatically-in-linux

3、NetworkManager

https://wiki.archlinux.org/index.php/NetworkManager