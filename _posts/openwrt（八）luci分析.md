---
title: openwrt（八）luci分析
date: 2018-04-11 21:59:43
tags:
	- openwrt

---



luci是openwrt的web管理系统。是用lua写的。

代码在/www目录下。

```
/usr/sbin/uhttpd -f -h /www -r LEDE -
```

web server是uhttpd。这个web server又是谁写的呢？跟thttpd区别何在呢？

github地址在这：

https://github.com/lewischeng-ms/uhttpd



暂时不深入看luci的代码了。

