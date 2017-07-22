---
title: shadowsocks之参数说明
date: 2017-07-23 00:01:49
tags:

	- shadowsocks

---

参数可以分为两类，一类是代理选项，一类是通用选项。

# 1. 代理选项

1、-c：指定配置文件。例如-c ss.conf

2、-s：指定服务器地址。默认是0.0.0.0。这个用默认就好了。

3、-p：指定端口。默认是8388。

4、-k：指定密码。

5、-m：指定加密方法。

6、-t：指定timeout时间。

7、-a：指定一次授权。

8、--fast-open。使用TCP_FASTOPEN，需要Linux3.7以上。

9、--workers。指定worker个数，*nix系统可用。

10、--forbidden-ip IPLIST。禁止某些ip连接。

11、--manager-address ADDR。不=很清楚。

12、prefer-ipv6。优先使用ipv6。



# 2. 通用选项

1、-h。显示帮助信息。

2、-d。start/stop/restart。表示daemon模式运行。

3、--pid-file PID_FILE。

4、--log-file LOG_FILE。

5、--user USER

6、-v，-vv。使用verbose模式。vv比v的信息更多。

7、-q，-qq。使用quiet模式。qq比q的信息更少。

8、--version。









