---
title: Linux之WiFi模块同时启动ap和sta模式
date: 2021-04-29 16:06:34
tags:
	- Linux
---

--

我觉得这个功能还是比较神奇的。

Realtek WiFi 模块是否能实现AP和station 模式同时启用，大家都均确定的说这是不能的。

后面网上看看，说可以的，于是找模块供应商咨询了一下，果然是可以的，

其实原厂驱动已经做好了，非常简单，流程如下：

1、在WiFi驱动Makefile文件里面加上EXTRA_CFLAGS += -DCONFIG_CONCURRENT_MODE 然后编译出WiFi驱动就**支持生成wlan0 和wlan1 双网络节点了。**



注意修改相关文档wlan0 用于STA，wlan1 用于AP。

还有用route add -net 192.168.43.0 netmask 255.255.255.0 gw 192.168.43.1 命令因为给AP（wlan01） 设置默认网关能ping通测试手机，因为默认路由已经给了wlan0，wlan1也是需要自己手动设置的。






参考资料

1、

https://blog.csdn.net/gooogleman/article/details/91968260

2、基于Linux wpa_supplicant  wpa_cli 工具调试WiFi sta 网络连接

https://blog.csdn.net/gooogleman/article/details/90693117

3、基于Linux WiFi ap 的hostapd 工具的使用方法

https://blog.csdn.net/gooogleman/article/details/90693362