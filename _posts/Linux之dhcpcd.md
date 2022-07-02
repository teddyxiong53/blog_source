---
title: Linux之dhcpcd
date: 2018-08-23 16:22:35
tags:
	- Linux

---



dhcpcd是 dhcp client daemon的缩写。是dhcp 客户端。



```
-b或者--background
	后台运行。
-c或者--script xx
	指定脚本文件。
-d或者--debug
	调试模式。
-K或者--nolink
	这个不是很推荐。
	但是有效果。
```



```
-K, --nolink
             Don't receive link messages for carrier status.  You should only have to use this with buggy device drivers or running dhcpcd through a network manager.
```



```
If any interface reports a working carrier then dhcpcd will try and obtain a lease before forking to the background, otherwise it will fork right away.  This behaviour can be mod‐
     ified with the -b, --background and -w, --waitip options.
```



有些回调脚本在这个目录下。这些都是默认的脚本。

```
/lib/dhcpcd/dhcpcd-hooks # ls
01-test         20-resolv.conf  50-ntp.conf
02-dump         30-hostname
```

使用了-c选项后，就不会用这些了。

```
-c, --script script
             Use this script instead of the default /lib/dhcpcd/dhcpcd-run-hooks.
```



avahi是什么？





 这样启动的时候，如果没有连接网线，会导致dhcpcd配置超时，启动失败,程序退出。



1、当我们的客户机无法找到 DHCP服务器时，它将从 TCP/IP的 B类网段 169.254.0.0中挑选一个 IP地址作为自己的 IP地址，而继续每隔 5分钟尝试与 DHCP服务器进行通信。（这里的这个 B类地址被称为 APIPA，即自动分配私有 IP地址！）

# 参考资料

1、

https://bbs.archlinux.org/viewtopic.php?id=103278

2、

https://www.baidu.com/link?url=uszStiQ3oDsijAWyEKWVW3Up90wamA0lMAQc6EUp1YyNjI1MixXn0xAsPVyNQn3S3-1Qf9ydSjojmh_uIlIjRa&wd=&eqid=8d2d33e00001200a000000065b7e7383/

3、

参数详解

https://blog.csdn.net/haomcu/article/details/8446109

4、

dhcpcd 移植

https://www.cnblogs.com/helloworldtoyou/p/5457504.html

5、Linux 使用 iw, wpa_supplicant, dhcpcd 连接 WiFi

https://blog.csdn.net/qq_36485711/article/details/106018940