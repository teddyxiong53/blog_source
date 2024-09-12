---
title: openwrt之在windows抓openwrt的包
date: 2020-09-21 13:36:30
tags:
	- 路由器

---



```
plink.exe -ssh -pw admin root@192.168.1.1 "tcpdump -ni br-lan -s 0 -w - not port 22" | "C:\Program Files (x86)\Wireshark\Wireshark.exe" -k -i -
```



参考资料

1、Windows 下利用openwrt网关进行wireshark抓包

http://www.voidcn.com/article/p-dydldyla-dr.html